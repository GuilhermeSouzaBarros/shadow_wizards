import requests

KEY = "$2a$10$vkEdT6UDF5I/XOTwBxyO5.jqI0Rc2cc97jRDkqUOCjxZOv5rrclZG"
BIN_ID = "678fa533ad19ca34f8f20642"
API_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

def set_address(ip:str, port:int):
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": KEY
    }
    data = {"server_ip": ip, "server_port": port}

    response = requests.put(API_URL, json=data, headers=headers)
    if response.status_code != 200:
        print("[ ! ] Erro ao atualizar IP:", response.text)

def get_address():
    headers = {
        "X-Master-Key": KEY
    }

    response = requests.get(API_URL + "/latest", json=None, headers=headers).json()
    return response["record"]["server_ip"], response["record"]["server_port"]
