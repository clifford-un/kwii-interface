from zeep import Client
import json

url = "http://localhost:8420/?wsdl"
client = Client(url)
# result = client.service.send_message("Juan", "Japon Campeón")
result = client.service.get_messages("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NjEzNDUyODEsImV4cCI6MTU2MTQzMTY4MSwiYXVkIjoiQ2xpZmZvcmQtVU4iLCJpc3MiOiJDbGlmZm9yZC1VTiIsInN1YiI6Ikdyb3VwQiJ9.t5rOzV0D2zNSCXRpJFR5p2rx2QYLK567jgK4LD8bYqw")
print(result)
