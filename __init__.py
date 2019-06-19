from flask import Flask, request
import requests
from config import PORT

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


def test_graphql(query):
    request = requests.post("http://34.73.50.226/kwii_api/graphql", json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

if __name__ == "__main__":
    query = """
    {
        authTest {
            message
        }
    }
    """
    graphql = test_graphql(query)
    print(graphql["data"]["authTest"]["message"])
    app.run(port=PORT)