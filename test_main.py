from fastapi.testclient import TestClient
from main import app # Actual code is in main.py

client = TestClient(app)

def test_add_book():
    response = client.post( "/book",
        json={"id": 1, "title": "1984", "author": "George Orwell", "publisher": "Secker & Warburg"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "1984", "author": "George Orwell", "publisher": "Secker & Warburg"}
    ]

def test_get_books():
    response = client.get("/list")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_book():
    response = client.get("/book/1")
    assert response.status_code == 200
    assert response.json()["title"] == "1984"

def test_modify_book():
    response = client.put(
        "/book/1",
        json={"id": 1, "title": "Animal Farm", "author": "George Orwell", "publisher": "Secker & Warburg"},
    )
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Animal Farm"

def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json() == []
    
    
# To run the tests, use the command:
# pytest test_main.py -W ignore::DeprecationWarning
