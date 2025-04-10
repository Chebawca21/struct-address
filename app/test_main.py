from fastapi.testclient import TestClient
from app.models import Status

from .main import app

client = TestClient(app)

def test_unknown_process():
    response = client.get("/result/0")
    assert response.status_code == 200
    assert response.json() == {"uuid": 0,
                               "status": Status.unknown,
                               "imie_nazwisko": None,
                               "ulica": None,
                               "numer_domu": None,
                               "kod_pocztowy": None,
                               "miasto": None,
                               "wojewodztwo": None
                               }

def test_invalid_uuid():
    response = client.get("/result/a")
    assert response.status_code == 422

def test_struct():
    response = client.post("/struct", params={'adr': 'Aleksandra Nowak ul. Kwiatowa 17/5 50-123 Wrocław'})
    assert response.status_code == 200
    assert response.json() == {"adr": "Aleksandra Nowak ul. Kwiatowa 17/5 50-123 Wrocław",
                              "uuid": 0}

def test_struct_address():
    client.post("/struct", params={'adr': 'Aleksandra Nowak ul. Kwiatowa 17/5 50-123 Wrocław Dolnośląskie'})
    response = client.get("/result/0")
    assert response.status_code == 200
    assert response.json() == {"uuid": 0,
                               "status": "DONE",
                               "imie_nazwisko": "Aleksandra Nowak",
                               "ulica": "ul. Kwiatowa",
                               "numer_domu": "17/5",
                               "kod_pocztowy": "50-123",
                               "miasto": "Wrocław",
                               "wojewodztwo": "Dolnośląskie"
                               }

def test_missing_voivodeship():
    client.post("/struct", params={'adr': 'Aleksandra Nowak ul. Kwiatowa 17/5 50-123 Wrocław'})
    response = client.get("/result/0")
    assert response.status_code == 200
    assert response.json() == {"uuid": 0,
                               "status": "DONE",
                               "imie_nazwisko": "Aleksandra Nowak",
                               "ulica": "ul. Kwiatowa",
                               "numer_domu": "17/5",
                               "kod_pocztowy": "50-123",
                               "miasto": "Wrocław",
                               "wojewodztwo": "Dolnośląskie"
                               }

def test_missing_city():
    client.post("/struct", params={'adr': 'Aleksandra Nowak ul. Kwiatowa 17/5 50-123 Dolnośląskie'})
    response = client.get("/result/0")
    assert response.status_code == 200
    assert response.json() == {"uuid": 0,
                               "status": "DONE",
                               "imie_nazwisko": "Aleksandra Nowak",
                               "ulica": "ul. Kwiatowa",
                               "numer_domu": "17/5",
                               "kod_pocztowy": "50-123",
                               "miasto": "Wrocław",
                               "wojewodztwo": "Dolnośląskie"
                               }