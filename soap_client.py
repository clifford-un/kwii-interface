from zeep import Client
import json
from flask import Flask, request
import requests

url = "http://0.0.0.0:8420/?wsdl"
client = Client(url)


def test_wsdl():
    # result = client.service.send_message("Juan", "Japon Campeón")
    result = client.service.get_messages()
    return result


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
    return test_wsdl()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8425)

