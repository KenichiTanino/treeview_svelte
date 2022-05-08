from fastapi import FastAPI
from fastapi.testclient import TestClient

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api import app

# app = FastAPI()

client = TestClient(app)


def test_tree_main():
    response = client.get("/ft")
    # print(response.json())
    assert response.status_code == 200
    assert response.json() == [{'id': 0, 'type': 'Folder', 'text': '/', 'children': [{'id': 1, 'type': 'Folder', 'text': '/b', 'children': [{'id': 2, 'type': 'DocumentBlank', 'text': '/b/c'}]}, {'id': 3, 'type': 'Folder', 'text': '/sets', 'children': []}, {'id': 4, 'type': 'Folder', 'text': '/sets/sets2', 'children': [{'id': 5, 'type': 'DocumentBlank', 'text': '/sets/sets2/test.txt'}]}, {'id': 6, 'type': 'DocumentBlank', 'text': '/a'}, {'id': 7, 'type': 'DocumentBlank', 'text': '/setting.txt'}]}] 


def test_content_read():
    response = client.get("/ft/7")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'content': "dGVzdGZpbGU=", 'name': '/setting.txt'}