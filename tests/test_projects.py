def auth_token(client):
    client.post("/api/v1/auth/register", json={
        "email": "test2@test.com",
        "password": "pass123",
        "full_name": "Test User 2"
    })

    response = client.post("/api/v1/auth/login", data={
        "username": "test2@test.com",
        "password": "pass123"
    })

    return response.json()["access_token"]


def test_create_and_list_projects(client):
    token = auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/projects", json={
        "name": "My Test Project",
        "description": "Test description"
    }, headers=headers)

    assert response.status_code == 201
    project = response.json()
    assert project["name"] == "My Test Project"

    response = client.get("/api/v1/projects", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
