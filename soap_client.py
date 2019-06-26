from flask import Flask, request, Response
import json
import requests
import xmltodict


def wsdl_get_posts(email):
    url = "http://35.232.95.82:3006/soapservice"
    # email = "integracion@arqui.com"
    headers = {"content-type": "text/xml"}
    body = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:examples:postservice">
    <soapenv:Header/>
    <soapenv:Body>
        <urn:getPosts soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <email xsi:type="xsd:string">{0}</email>
        </urn:getPosts>
    </soapenv:Body>
    </soapenv:Envelope>
    """.format(
        email
    )
    response = requests.post(url, data=body, headers=headers)

    if response.status_code == 200:
        text = response.text
        result = xmltodict.parse(text)
        result = json.dumps(
            result["soap:Envelope"]["soap:Body"]["tns:getPostsResponse"]
        )
        return Response(response=result, status=200, mimetype="application/json")
    else:
        result = '{"error": "Correo invalido"}'
        return Response(response=result, status=500, mimetype="application/json")


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World! (kwii-interface)"


@app.route("/getPosts/<email>")
def getPosts(email):
    return wsdl_get_posts(email)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8425)

