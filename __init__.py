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


def test_graphql(query, variables):
    request = requests.post(
        "http://34.73.50.226/kwii_api/graphql",
        json={"query": query, "variables": variables},
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                request.status_code, query
            )
        )


if __name__ == "__main__":
    username = "higuaran"
    password = "HolaMundo"
    query = """
    mutation createToken($username: String!, $password: String!) {
        createToken(user: {userName: $username, password: $password}) {
            jwt, user_id
        }
    }"""
    variables = {"username": username, "password": password}
    graphql = test_graphql(query, variables)
    print(graphql["data"])
    app.run(port=PORT)
