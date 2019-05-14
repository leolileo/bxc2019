import http.client

# headers = {"accept": "application/json", "x-cr-api-token": "e7f6e462a0e84cbab0dcae505cf54239",
#          "Authorization": "Basic SEFYXENyZWF0aXZlTWVkdXNhOmVYeVQ5RiUzK0lvWXkmNw=="}
import time

connection = http.client.HTTPConnection('hackthonbxc2019.herokuapp.com', 8000)


# The data model

def getData():
    connection.request("GET", "/status/alert")
    connection.close()


getData()
