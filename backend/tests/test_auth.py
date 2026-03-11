import os
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from main import app

load_dotenv()

# This utilizes the TestClient to hit our API directly in tests.
client = TestClient(app)

# Test Data based on seed.py
USERS_TO_TEST = [
    {"email": os.environ.get("ADMIN_EMAIL", "admin@campus.com"), "password": os.environ.get("ADMIN_PASSWORD", "admin123"), "expected_role": "admin"},
    {"email": "student1@campus.com", "password": "student123", "expected_role": "student"},
    {"email": "lecturer1@campus.com", "password": "lecturer123", "expected_role": "lecturer"},
]

class TestAuth:
    """
    Integration tests for the Authentication router.
    Requires the database to be seeded via seed.py.
    """

    @pytest.mark.parametrize("user_data", USERS_TO_TEST)
    def test_login_and_verify_jwt_roles(self, user_data):
        email = user_data["email"]
        password = user_data["password"]
        expected_role = user_data["expected_role"]

        # 1. Test Login to get the JWT token
        login_payload = {
            "email": email,
            "password": password
        }
        
        login_response = client.post("/api/auth/login", json=login_payload)
        
        assert login_response.status_code == 200, f"Login failed for {email}: {login_response.text}"
        
        token_data = login_response.json()
        assert "access_token" in token_data, "Token must be present in response"
        assert token_data["role"] == expected_role, f"Expected role {expected_role}, got {token_data.get('role')}"
        
        access_token = token_data["access_token"]

        # 2. Test Verification endpoint using the JWT token
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        verify_response = client.get("/api/auth/verify", headers=headers)
        
        assert verify_response.status_code == 200, f"/verify request failed for {email}"
        
        verify_data = verify_response.json()
        assert verify_data["valid"] is True, "Token should be flagged as valid"
        assert verify_data["role"] == expected_role, f"JWT embedded role should be {expected_role}"
        
        # 3. Check for specific ID inclusion based on roles
        if expected_role == "student":
            assert verify_data["student_id"] is not None, "Student token must have student_id"
        elif expected_role == "lecturer":
            assert verify_data["lecturer_id"] is not None, "Lecturer token must have lecturer_id"
        
        # Check that user_id is present for all valid auths
        assert verify_data["user_id"] is not None, "All valid tokens must attach a user_id"
