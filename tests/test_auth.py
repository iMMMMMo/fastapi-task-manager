def test_register_and_login(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "pass123",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == "test@test.com"

    response = client.post("/api/v1/auth/login", data={
        "username": "test@test.com",
        "password": "pass123"
    })
    assert response.status_code == 200

    token_data = response.json()
    assert "access_token" in token_data

    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"
