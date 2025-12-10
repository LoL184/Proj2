import requests


def greet(name: str) -> str:
    return f"Hello, {name}!"


def fetch_status(url: str) -> str:
    return str(requests.get(url, timeout=5))
