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
    client.post("/struct", params={'adr': 'Aleksandra Nowak ul. Kwiatowa 17/5 50-123 Wrocław dolnośląskie'})
    response = client.get("/result/0")
    assert response.status_code == 200
    assert response.json() == {"uuid": 0,
                               "status": "DONE",
                               "imie_nazwisko": "Aleksandra Nowak",
                               "ulica": "ul. Kwiatowa",
                               "numer_domu": "17/5",
                               "kod_pocztowy": "50-123",
                               "miasto": "Wrocław",
                               "wojewodztwo": "dolnośląskie"
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
                               "wojewodztwo": "dolnośląskie"
                               }

def test_missing_city():
    client.post("/struct", params={'adr': 'Aleksandra Nowak ul. Kwiatowa 17/5 50-123 dolnośląskie'})
    response = client.get("/result/0")
    assert response.status_code == 200
    assert response.json() == {"uuid": 0,
                               "status": "DONE",
                               "imie_nazwisko": "Aleksandra Nowak",
                               "ulica": "ul. Kwiatowa",
                               "numer_domu": "17/5",
                               "kod_pocztowy": "50-123",
                               "miasto": "Wrocław",
                               "wojewodztwo": "dolnośląskie"
                               }

def test_response():
    client.post("/struct", params={'adr': 'Wiesława Frano ul. Kwiatowa 17/5 50-123 dolnośląskie'})
    client.post("/struct", params={'adr': 'Paweł Bandura ul. Bolesława Chrobrego 145 42-500 Będzin'})
    client.post("/struct", params={'adr': 'Iwona Bagińska ul. Gołębia 3 15-336 Białystok'})
    client.post("/struct", params={'adr': 'Bernard Kątny ul. J. Hallera 11  07-412 Ostrołęka'})
    client.post("/struct", params={'adr': 'Antonina Duczyńska ul. Podjazd 78 81-805 Sopot'})
    client.post("/struct", params={'adr': 'Izydor Jagodziński ul. Kilińskiego Jana 133 85-670 Bydgoszcz'})
    client.post("/struct", params={'adr': 'Judyta Cisło  ul. Moniuszki Stanisława 54 41-406 Mysłowice'})
    client.post("/struct", params={'adr': 'Klara Sugalska ul. Zakręt 93 02-907'})
    client.post("/struct", params={'adr': 'Bartosz Kaczmarski ul. Wiejska 17 44-338 Jastrzębie-zdrój'})
    response = client.post("/struct", params={'adr': 'Stefan Żaczek ul. Morcinka Gustawa 143 40-124'})
    id = response.json()["uuid"]
    response = client.get(f"/result/{id}")
    assert response.status_code == 200
    assert response.json() == {"uuid": id,
                               "status": "DONE",
                               "imie_nazwisko": "Stefan Żaczek",
                               "ulica": "ul. Morcinka Gustawa",
                               "numer_domu": "143",
                               "kod_pocztowy": "40-124",
                               "miasto": "Katowice",
                               "wojewodztwo": "śląskie"
                               }