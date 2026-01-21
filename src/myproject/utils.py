import json

'''import requests
from fastapi import FastAPI


def greet(name: str) -> str:
    return f"Hello, {name}!"


def fetch_status(url: str) -> str:
    return str(requests.get(url, timeout=5))


def wrong_one():
    r = requests.get(url="https://jsonplaceholder.typicode.com/xyz", timeout=5)
    return f"Error {r.status_code}"

app = FastAPI(title="Advice wrapper")

@app.get("/advice")
def day_advice():
    try:
        return requests.get("https://api.adviceslip.com/advice", timeout=5).json()["slip"]["advice"]
    except ValueError:
        return "Error Unable to connect."


@app.get("/ses_advice")
def session_day_advices():
    with requests.Session() as session:
        advices = []
        for i in range(3):
            r = session.get("https://api.adviceslip.com/advice", timeout=5)
            r.raise_for_status()
            advices.append(r.json()['slip']["advice"])
        return tuple(advices)


@app.get("/random_dog_url")
def get_random_dog_url():
    r = requests.get(url="https://dog.ceo/api/breeds/image/random", timeout=5)
    r.raise_for_status
    return r.json()["message"]
'''

# Функции, для преобразования данных из JSON в dict и обратно
def dict_list_to_json(dict_list, filename):
    pass

def json_to_dict_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)