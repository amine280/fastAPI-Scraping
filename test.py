from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_scrapping():
    response = client.get("/scrap/lifemovie")
    assert response.status_code == 200