from shortener.main import app
import pytest
import json


headers = {'Content-Type': 'application/json'}

def test_encode():
    data = {'url':'google.com'}

    response = app.test_client().post('/encode', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json['short_url'] == 'localhost:5000/d4c9d902'


def test_decode():
    data = {'short_code': 'd4c9d902'}

    response = app.test_client().get('/decode', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json['original_url'] == 'google.com'


def test_redirect():
    response = app.test_client().get('/d4c9d902', headers=headers)
    assert response.status_code == 302