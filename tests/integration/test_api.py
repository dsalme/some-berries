import pytest


class TestHomeApi:
    def test_home_page(self, client):
        req = client.get("/")
        assert req.status_code == 200


class TestBerriesApi:

    def test_berries_page_success(self, client):
        req = client.get("/allBerryStats")
        assert req.status_code == 200

