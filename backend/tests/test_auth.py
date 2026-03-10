import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
import os

client = TestClient(app)

# We use the existing admin credentials for testing or create a test user
test_email = "testuser@example.com"
test_password = "testpassword123"
test_id_number = "TEST-001"

def test_register_user():
    """Test user registration."""
    # First, try to delete if exists to ensure clean state (optional, or just use unique ID)
    response = client.post(
        "/api/auth/register",
        json={
            "email": test_email,
            "password": test_password,
            "id_number": test_id_number
        }
    )
    # If user already exists (409), that's fine for this test structure
    assert response.status_code in [201, 409]
    if response.status_code == 201:
        assert response.json()["email"] == test_email

def test_login_user():
    """Test user login."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": test_email,
            "password": test_password
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]

def test_verify_token():
    """Test token verification."""
    # First login to get a token
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": test_email,
            "password": test_password
        }
    )
    token = login_response.json()["access_token"]
    
    # Now verify
    response = client.get(
        "/api/auth/verify",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["valid"] is True

def test_login_invalid_credentials():
    """Test login with wrong password."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": test_email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
