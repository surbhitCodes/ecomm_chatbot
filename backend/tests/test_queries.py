# backend/tests/test_queries.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

API_KEY = "boom-boom-arbor-1234"

def test_material_query():
    response = client.post(
        "/queries/",
        json={
            "query": "What is the best pressure-treated lumber for outdoor decking considering cost and durability?"
        },
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "answer" in json_data
    assert "sources" in json_data

def test_project_planning_estimate():
    response = client.post(
        "/project-planning/estimate",
        json={
            "description": "Building a 2000 sq ft residential home with a two-car garage."
        },
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "materials" in json_data
    assert "total_cost" in json_data
    assert "details" in json_data

def test_technical_support():
    response = client.post(
        "/technical-support/",
        json={
            "question": "How do I install pressure-treated lumber to prevent rot?"
        },
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "answer" in json_data
    assert "references" in json_data
