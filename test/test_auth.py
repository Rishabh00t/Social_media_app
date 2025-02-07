# from fastapi.testclient import TestClient
# from src.app import app
# client = TestClient(app)
# def test_read_root():
#     reponse = client.get("/")
#     assert reponse.status_code == 200
#     assert reponse.json() == {"message": "Hello, World!"}

# def test_user_create_root():
#     response = client.post(
#         "/signup",
#         json={
#             "username": "testuser1",
#             "password": "TestPassword123",
#             "email": "test1@example.com"
#         }
#     )

#     assert response.status_code == 200  # Check if the request was successful

#     data = response.json()  # Extract response JSON

#     # Validate the response structure
#     assert data["success"] is True
#     assert data["message"] == "Account successfully created. OTP has been sent, and expires in 5 minutes."
#     assert "user" in data
#     assert isinstance(data["user"]["id"], int)
#     assert data["user"]["username"] == "testuser1"
#     assert data["user"]["email"] == "test1@example.com"
#     assert "otp_code" in data["user"]
#     assert "Access-token" in data
#     assert isinstance(data["Access-token"], str)


# def test_user_delete_root():
#     # Use a valid access token (ensure it's still valid)
#     access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEiLCJpZCI6MjEsImV4cCI6MTczOTc4NzE3OX0.IAhTtAeDQox_exZcN7yHdhirZ5Ol4WcQT-l7PaQojqo"

#     user_id = 21  # Ensure this user exists before deleting
#     response = client.delete(
#         f"/deleteuser/{user_id}",
#         headers={"Authorization": f"Bearer {access_token}"}
#     )

#     # Validate response
#     assert response.status_code == 200
#     data = response.json()

#     assert data["success"] is True
#     assert data["message"] == f"User with ID {user_id} successfully deleted."
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEyIiwiaWQiOjIyLCJleHAiOjE3Mzg5MjgxNTZ9.46fwudRS6lKjnNT5HwXFowJXrzqXSR1nnATwxqtkyqc"

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_user_create():
    response = client.post("/signup", json={"username": "testuser12", "password": "TestPassword123", "email": "test12@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] and "user" in data and "Access-token" in data

def test_user_delete():
    user_id = 22  # Ensure this user exists
    response = client.delete(f"/deleteuser/{user_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200 and response.json()["success"]

