from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, AnyDict
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# from typing import Dict
import requests


def send_graphql(query, variables):
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


def transform_data(graphql_data=[]):
    result = []
    for value in graphql_data:
        username, message = value["chat_text"].split("+", 1)
        date = value["chat_date_stamp"]
        result.append({"username": username, "message": message, "date": date})
    return result


class KwiiService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def send_message(ctx, username, message):
        """
        Kwii send message

        @param username the username who sends the message
        @param message the text to send
        """

        query = """
        mutation createChat($chat_text: String!, $token: String!){
            createChat(chat: {chat_user_origin: 5,
            chat_room_id: "5d0e838124aa9a000170b7bd",
            chat_text: $chat_text},
            token: $token
            username: "GroupB") {
                chat_user_origin, chat_room_id, chat_text, chat_date_stamp
            }
        }"""
        variables = {
            "chat_text": username + "+" + message,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NjEyMjk4MzEsImV4cCI6MTU2MTMxNjIzMSwiYXVkIjoiQ2xpZmZvcmQtVU4iLCJpc3MiOiJDbGlmZm9yZC1VTiIsInN1YiI6Ikdyb3VwQiJ9.4bC7Q13EMjvhGlI-DS3Qy-vEkMOshMyrBk_KDLxcrRY",
        }
        result = send_graphql(query, variables)
        if result["data"] is None:
            return "Something went wrong!"
        else:
            return "Message sent"

    @rpc(_returns=Unicode)
    def get_messages(ctx):
        """
        Kwii get all messages

        @return an array with dictionaries (json) {"username": "", "message": "", date: ""} 
        """

        query = """
        query chatById($token: String!){
            chatById(chat_room_id: "5d0e838124aa9a000170b7bd",
            token: $token
            username: "GroupB") {
                chat_text, chat_date_stamp
            }
        }"""
        variables = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NjEyMjk4MzEsImV4cCI6MTU2MTMxNjIzMSwiYXVkIjoiQ2xpZmZvcmQtVU4iLCJpc3MiOiJDbGlmZm9yZC1VTiIsInN1YiI6Ikdyb3VwQiJ9.4bC7Q13EMjvhGlI-DS3Qy-vEkMOshMyrBk_KDLxcrRY"
        }
        result = send_graphql(query, variables)
        if result["data"] is None:
            return "Something went wrong!"
        else:
            result = result["data"]["chatById"]
            data = transform_data(result)
            return str(data)


application = Application(
    [KwiiService],
    "kwii-interface",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_application = WsgiApplication(application)


if __name__ == "__main__":
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("spyne.protocol.xml").setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8420")
    logging.info("wsdl is at: http://localhost:8420/?wsdl")

    server = make_server("127.0.0.1", 8420, wsgi_application)
    server.serve_forever()
