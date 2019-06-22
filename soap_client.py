from zeep import Client
import json

url = "http://localhost:8420/?wsdl"
client = Client(url)
# result = client.service.send_message("Juan", "Japon Campeón")
result = client.service.get_messages()
print(result)
