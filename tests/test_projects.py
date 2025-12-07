def get_token(client, email="user@test.com", password="pass123", fullname="User"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": fullname,
    })

    response = client.post("/api/v1/auth/login", data={
        "username": email,
        "password": password
    })

    return {"Authorization": f"Bearer {response.json()['access_token']}"}


#
# CREATE + LIST
#

def test_create_project_success(client):
    headers = get_token(client)

    response = client.post("/api/v1/projects", json={
        "name": "My Test Project"
    }, headers=headers)

    assert response.status_code == 201
    assert response.json()["name"] == "My Test Project"


def test_list_projects_returns_only_own_items(client):
    headers = get_token(client)

    client.post("/api/v1/projects", json={"name": "A"}, headers=headers)
    client.post("/api/v1/projects", json={"name": "B"}, headers=headers)

    response = client.get("/api/v1/projects", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


#
# GET SINGLE
#

def test_get_project_success(client):
    headers = get_token(client)

    r = client.post("/api/v1/projects", json={"name": "Solo Project"}, headers=headers)
    project_id = r.json()["id"]

    response = client.get(f"/api/v1/projects/{project_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == project_id


def test_get_nonexistent_project_returns_404(client):
    headers = get_token(client)

    response = client.get("/api/v1/projects/999999", headers=headers)

    assert response.status_code == 404


def test_get_project_owned_by_another_user_forbidden(client):
    owner_headers = get_token(client, "owner@test.com", fullname="Owner")
    other_headers = get_token(client, "other@test.com", fullname="Other")

    r = client.post("/api/v1/projects", json={"name": "Private Project"}, headers=owner_headers)
    project_id = r.json()["id"]

    response = client.get(f"/api/v1/projects/{project_id}", headers=other_headers)

    assert response.status_code == 403


#
# UPDATE
#

def test_update_project_success(client):
    headers = get_token(client)

    r = client.post("/api/v1/projects", json={"name": "Old Name"}, headers=headers)
    project_id = r.json()["id"]

    response = client.put(f"/api/v1/projects/{project_id}", json={"name": "Updated"}, headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_update_nonexistent_project_returns_404(client):
    headers = get_token(client)

    response = client.put("/api/v1/projects/123456", json={"name": "Updated"}, headers=headers)

    assert response.status_code == 404


def test_update_project_owned_by_other_user_forbidden(client):
    owner_headers = get_token(client, "owner@test.com")
    other_headers = get_token(client, "other@test.com")

    r = client.post("/api/v1/projects", json={"name": "Private"}, headers=owner_headers)
    project_id = r.json()["id"]

    response = client.put(f"/api/v1/projects/{project_id}", json={"name": "Hack Attempt"}, headers=other_headers)

    assert response.status_code == 403


#
# DELETE
#

def test_delete_project_success(client):
    headers = get_token(client)

    r = client.post("/api/v1/projects", json={"name": "ToDelete"}, headers=headers)
    project_id = r.json()["id"]

    delete_response = client.delete(f"/api/v1/projects/{project_id}", headers=headers)
    assert delete_response.status_code == 204

    r2 = client.get(f"/api/v1/projects/{project_id}", headers=headers)
    assert r2.status_code == 404


def test_delete_nonexistent_project_returns_404(client):
    headers = get_token(client)

    response = client.delete("/api/v1/projects/999999", headers=headers)

    assert response.status_code == 404


def test_delete_project_owned_by_other_user_forbidden(client):
    owner_headers = get_token(client, "owner@test.com")
    other_headers = get_token(client, "other@test.com")

    r = client.post("/api/v1/projects", json={"name": "Secret"}, headers=owner_headers)
    project_id = r.json()["id"]

    response = client.delete(f"/api/v1/projects/{project_id}", headers=other_headers)

    assert response.status_code == 403
