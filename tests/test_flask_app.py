import pytest
from app import create_app
import csv
from dateutil import parser
import math


@pytest.fixture
def flask_client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture
def meter_usage():
    with open("./grpc_server/data/meterusage.1643022756.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            {
                "time": parser.parse(row["time"], ignoretz=True),
                "meterusage": float(row["meterusage"]),
            }
            for row in reader
        ]


def test_api_status_code(flask_client):
    response = flask_client.get("/usage/data")
    assert response.status_code == 200


def test_get_usage_data(flask_client, meter_usage):
    limit = 10
    response = flask_client.get(f"/usage/data?limit={limit}")
    json_data = response.get_json().get("data", [])
    assert response.status_code == 200
    assert len(json_data) == limit
    for index, row in enumerate(meter_usage[:limit]):
        assert parser.parse(json_data[index]["time"], ignoretz=True) == row["time"]
        assert json_data[index]["meterusage"] == row["meterusage"]


def test_all_data(flask_client, meter_usage):
    response = flask_client.get("/usage/data")
    json_data = response.get_json().get("data", [])
    assert response.status_code == 200
    assert len(json_data) == len(meter_usage)
    for index, row in enumerate(meter_usage):
        assert parser.parse(json_data[index]["time"], ignoretz=True) == row["time"]
        # Ignoring NaN value for testing
        if math.isnan(json_data[index]["meterusage"]) != math.isnan(row["meterusage"]):
            assert json_data[index]["meterusage"] == row["meterusage"]
