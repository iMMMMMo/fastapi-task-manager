def test_register_and_login(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "pass123"
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


def test_login_fail_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "wrong@test.com",
        "password": "pass123"
    })

    response = client.post("/api/v1/auth/login", data={
        "username": "wrong@test.com",
        "password": "incorrect"
    })

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_register_duplicate_user(client):
    payload = {
        "email": "duplicate@test.com", 
        "password": "pass123"
    }

    r1 = client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code == 400
    assert "already" in r2.json()["detail"].lower()

