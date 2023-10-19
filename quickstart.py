from __future__ import print_function

import os.path
import codecs
import json

import time

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1wt4qH0_KMv36-nbGbuwRvZjaLrNaPBYPOj5GPtgE48I'
SAMPLE_SEARCH = 'B2:B'
SAMPLE_ASINS = 'A2:A'
SEMPLA_DATA = 'B1:1000'
SEMPLA_DATE = 'C1:1'

def auth():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_values(ID):
    creds = auth()
    data = {

    }
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=ID, range=SAMPLE_SEARCH).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        print(rows)
        data["search"] = rows
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

    try:
        ##service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=ID, range=SAMPLE_ASINS).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        print(rows)
        data["asin"] = rows
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

    return data


def main(new_data, ID):
    creds = auth()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=ID,
                                    range=SEMPLA_DATA).execute()
        data = result.get('values', [])
        values = []
        this_index = len(data[0])

        def data_correction(data, length):
            new_dt = data
            while len(data) != length :
                new_dt.append('')
            return new_dt
        
        if data[0][-1] == new_data[0] :
            for i in range(0, len(data)):
                ind = data[i]
                new_ind = data_correction(ind, this_index)
                new_ind[-1] = new_data[i]
                values.append(new_ind)

        else:
            print(f'Total num {this_index}')
            for index in range(0, len(data)):
                result_item = data[index]
                new_result_item = result_item
                
                new_result_item = data_correction(new_result_item, this_index)
            
                new_result_item.append(new_data[index])
                print(new_result_item)
                values.append(new_result_item)

        
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=ID, range=SEMPLA_DATA,
            valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")


        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
    except HttpError as err:
        print(err)

##get_values()
##main(['11.02.2023', '11', '10', '15'])