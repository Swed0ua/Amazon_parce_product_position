from flask import Flask
import requests

app = Flask(__name__)


@app.route("/req")
  
def convert():
    
    return 'req!'
    currency = request.form.get("currency")

@app.route("/")
  
def user():
    ##main()
    return 'Hello!'
    currency = request.form.get("currency")


app.run(debug = True)