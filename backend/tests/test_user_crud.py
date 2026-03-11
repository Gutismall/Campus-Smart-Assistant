import os
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from main import app

load_dotenv()

client = TestClient(app)

def get_admin_headers():
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@campus.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    
    login_response = client.post("/api/auth/login", json={
        "email": admin_email,
        "password": admin_password
    })
    
    assert login_response.status_code == 200, "Setup failed: Could not log in as admin."
    token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

class TestUserCRUD:
    def test_full_user_crud_and_admin_security(self):
        headers = get_admin_headers()
        
        # 1. Test POST: Create generic user
        new_user = {
            "email": "crud_test@university.edu",
            "id_number": "CRUD12345",
            "password": "testpassword",
            "is_system_admin": False
        }
        
        create_res = client.post("/api/data/users", json=new_user, headers=headers)
        assert create_res.status_code == 200, f"Expected 200, got {create_res.status_code}. Response: {create_res.text}"
        
        created_data = create_res.json()
        assert created_data["email"] == new_user["email"]
        assert "id" in created_data
        
        user_id = created_data["id"]
        
        # 2. Test GET: Retrieve list and find new user
        get_res = client.get("/api/data/users", headers=headers)
        assert get_res.status_code == 200
        users_list = get_res.json()
        
        found = any(u["id"] == user_id for u in users_list)
        assert found, "Created user was not found in the users list"
        
        # 3. Test PUT: Update the user
        update_user = {
            "email": "crud_updated@university.edu",
            "id_number": "CRUD123456",
            "password": "newpassword123",
            "is_system_admin": False
        }
        
        put_res = client.put(f"/api/data/users/{user_id}", json=update_user, headers=headers)
        assert put_res.status_code == 200, f"Expected 200, got {put_res.status_code}. Response: {put_res.text}"
        
        updated_data = put_res.json()
        assert updated_data["email"] == "crud_updated@university.edu"
        
        # 4. SECURITY TEST: Try to create a system admin
        evil_admin_payload = {
            "email": "hacker@university.edu",
            "id_number": "HACK666",
            "password": "hackedpassword",
            "is_system_admin": True
        }
        
        admin_create_res = client.post("/api/data/users", json=evil_admin_payload, headers=headers)
        assert admin_create_res.status_code == 403, "System should block creation of an admin"
        assert "Cannot create a new system administrator" in admin_create_res.text
        
        # 5. Test DELETE: Remove the crud test user
        del_res = client.delete(f"/api/data/users/{user_id}", headers=headers)
        assert del_res.status_code == 200
        
        # Verify it was completely deleted by attempting to update it again
        verify_del_res = client.put(f"/api/data/users/{user_id}", json=update_user, headers=headers)
        assert verify_del_res.status_code == 404, "User should be completely deleted"
