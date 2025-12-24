import requests
from fastapi import FastAPI


def greet(name: str) -> str:
    return f"Hello, {name}!"


def fetch_status(url: str) -> str:
    return str(requests.get(url, timeout=5))

app = FastAPI(title="Advice wrapper")

@app.get("/advice")
def day_advice():
    return {"advice": requests.get("https://api.adviceslip.com/advice", timeout=5).json()["slip"]["advice"]}
