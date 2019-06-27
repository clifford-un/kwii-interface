from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, AnyDict
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import os
import requests


def send_graphql(query, variables):
    request = requests.post(
        "http://kwii-api:5500/graphql",
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
    def login(ctx, username, password):
        """
        Kwii authenticate

        @return an error if username and password are incorrect or return a JWT.
        """

        query = """
        mutation createToken($userName: String!, $password: String!) {
            createToken(user: {userName: $userName, password: $password}) {
                jwt, user_id, user_name
            }
        }"""
        variables = {
            "userName": username,
            "password": password
        }
        result = send_graphql(query, variables)
        if result["data"] is None:
            return "Something went wrong!"
        else:
            return result["data"]["createToken"]["jwt"]

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def send_message(ctx, username, message, token):
        """
        Kwii send message

        @param username the username who sends the message
        @param message the text to send
        """

        query = """
        mutation createChat($chat_text: String!, $token: String!){
            createChat(chat: {chat_user_origin: 4,
            chat_room_id: "5d1421a1b9d82100018c3cc6",
            chat_text: $chat_text},
            token: $token
            username: "GroupB") {
                chat_user_origin, chat_room_id, chat_text, chat_date_stamp
            }
        }"""
        variables = {
            "chat_text": username + "+" + message,
            "token": token
        }
        result = send_graphql(query, variables)
        if result["data"] is None:
            return "Something went wrong!"
        else:
            return "Message sent"

    @rpc(Unicode, _returns=Unicode)
    def get_messages(ctx, token):
        """
        Kwii get all messages

        @return an String (format: array with dictionaries) {"username": "", "message": "", date: ""} 
        """

        query = """
        query chatById($token: String!){
            chatById(chat_room_id: "5d1421a1b9d82100018c3cc6",
            token: $token
            username: "GroupB") {
                chat_text, chat_date_stamp
            }
        }"""
        variables = {
            "token": token
        }
        result = send_graphql(query, variables)
        if result["data"]["chatById"] is None:
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

    server = make_server("0.0.0.0", 8420, wsgi_application)
    server.serve_forever()
