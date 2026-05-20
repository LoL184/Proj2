import pytest
import requests

r = requests.get('https://api.adviceslip.com/advice', timeout=5)
data = r.json()['slip']['advice']
print(data, len(data))

@pytest.fixture
def base_url() -> str:
    return "https://api.adviceslip.com/advice"

@pytest.fixture
def session():
    s = requests.Session()
    yield s
    s.close()

def test_api_is_alive(session, base_url):
    r = session.get(base_url, timeout=5)
    assert r.status_code == 200
    assert 'application/json' in r.headers['Content-Type']


def test_json_structure(session, base_url):
    # запрос -> json
    # проверить структуру:
    # data содержит ключ 'slip'
    # data['slip'] содержит ключи 'id' и 'advice'
    r = session.get(base_url, timeout=5)
    data = r.json()
    assert 'slip' in data
    assert 'id' in data['slip']
    assert 'advice' in data['slip']

def test_advice_is_non_empty_string(session, base_url):
    # проверить, что advice:
    # 1) это str
    # 2) длина >= 5
    r = session.get(base_url, timeout=5)
    data = r.json()['slip']['advice']
    l = len(data)
    assert data is str and l >= 5

def test_three_requests_with_session(session, base_url):
    for i in range(3):
        test_api_is_alive(session, base_url)
        test_json_structure(session, base_url)