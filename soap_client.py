from zeep import Client
import json
from flask import Flask, request
import requests

def test_wsdl():
    url = "http://localhost:8420/?wsdl"
    client = Client(url)
    # result = client.service.send_message("Juan", "Japon Campeón")
    result = client.service.get_messages()
    print(result)

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World! (kwii-interface)"

    
@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "POST":
        return request.json["Hola"]
    else:
        return "Chat GET"


@app.route("/user/<username>")
def profile(username):
    return "{}'s profile".format(username)

@app.route("/test")
def test():
    test_wsdl()

if __name__ == "__main__":
    app.run(port=8425)