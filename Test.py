import pytest
import requests
import datetime

date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

#Test users creation
def test_create_user():
    header = {
        'Content-Type': 'application/json',
        }
    url='http://127.0.0.1:8000/auth/register/'
    new_user = {"user_name": "testepy", "password": "1234"}
    response = requests.post(url,headers=header ,json=new_user)
    assert response.status_code == 201
    
#Test token generation
def test_create_token():
    url="http://127.0.0.1:8000/auth/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"}
    data = {'grant_type': 'password',
        'username': 'testepy',
        'password': '1234',
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string'}
    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 200
