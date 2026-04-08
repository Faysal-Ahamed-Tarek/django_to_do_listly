from getpass import getpass
import requests


auth_endpoint = "http://127.0.0.1:8000/auth/"
username = input("Enter your username: ")
password = getpass("Enter your password: ")


auth_response = requests.post(auth_endpoint, json = {"username" : username, "password" : password})
print(auth_response.json())

if auth_response.status_code == 200 :
    token = auth_response.json().get("token")
    headers = {
        "Authorization" : f"Token {token}"
    }
    endpoint = "http://127.0.0.1:8000/tasks/"
    response = requests.get(endpoint, headers=headers)
    print(response.json())