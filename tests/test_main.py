"""
Test for the main page using fastapi.testclient.
"""
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
