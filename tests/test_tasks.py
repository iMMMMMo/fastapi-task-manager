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


def create_project(client, headers, name="Project A"):
    r = client.post("/api/v1/projects", json={"name": name}, headers=headers)
    return r.json()["id"]


#
# CREATE TASK
#

def test_create_task_success(client):
    headers = get_token(client)
    project_id = create_project(client, headers)

    response = client.post("/api/v1/tasks", json={
        "title": "My Task",
        "project_id": project_id
    }, headers=headers)

    assert response.status_code == 201
    assert response.json()["title"] == "My Task"
    assert response.json()["project_id"] == project_id


def test_create_task_fails_if_project_not_found(client):
    headers = get_token(client)

    response = client.post("/api/v1/tasks", json={
        "title": "Task",
        "project_id": 99999
    }, headers=headers)

    assert response.status_code == 404


def test_create_task_fails_if_project_belongs_to_other_user(client):
    owner_headers = get_token(client, "owner@test.com")
    other_headers = get_token(client, "other@test.com")

    project_id = create_project(client, owner_headers)

    response = client.post("/api/v1/tasks", json={
        "title": "Hack",
        "project_id": project_id
    }, headers=other_headers)

    assert response.status_code == 403


def test_create_task_with_assignee_validation(client):
    headers = get_token(client)
    project_id = create_project(client, headers)

    response = client.post("/api/v1/tasks", json={
        "title": "Assigned",
        "project_id": project_id,
        "assignee_id": 999
    }, headers=headers)

    assert response.status_code == 404


#
# LIST TASKS
#

def test_list_tasks_returns_only_user_tasks(client):
    headers = get_token(client, "user1@test.com")
    other_headers = get_token(client, "user2@test.com")

    project1 = create_project(client, headers)
    project2 = create_project(client, other_headers)

    client.post("/api/v1/tasks", json={"title": "A", "project_id": project1}, headers=headers)
    client.post("/api/v1/tasks", json={"title": "B", "project_id": project2}, headers=other_headers)

    response = client.get("/api/v1/tasks", headers=headers)
    tasks = response.json()

    assert response.status_code == 200
    assert len(tasks) == 1
    assert tasks[0]["title"] == "A"


#
# GET SINGLE TASK
#

def test_get_task_success(client):
    headers = get_token(client)
    project_id = create_project(client, headers)

    r = client.post("/api/v1/tasks", json={"title": "One", "project_id": project_id}, headers=headers)
    task_id = r.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_nonexistent_task_returns_404(client):
    headers = get_token(client)

    response = client.get("/api/v1/tasks/99999", headers=headers)

    assert response.status_code == 404


def test_get_task_owned_by_other_user_forbidden(client):
    owner_headers = get_token(client, "owner@test.com")
    other_headers = get_token(client, "other@test.com")

    project_id = create_project(client, owner_headers)

    r = client.post("/api/v1/tasks", json={"title": "Private", "project_id": project_id}, headers=owner_headers)
    task_id = r.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}", headers=other_headers)

    assert response.status_code == 403


#
# UPDATE TASK
#

def test_update_task_success(client):
    headers = get_token(client)
    project_id = create_project(client, headers)

    r = client.post("/api/v1/tasks", json={"title": "Old", "project_id": project_id}, headers=headers)
    task_id = r.json()["id"]

    response = client.put(f"/api/v1/tasks/{task_id}", json={"title": "Updated"}, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_task_project_success(client):
    headers = get_token(client)

    project1 = create_project(client, headers, "P1")
    project2 = create_project(client, headers, "P2")

    r = client.post("/api/v1/tasks", json={"title": "Move", "project_id": project1}, headers=headers)
    task_id = r.json()["id"]

    response = client.put(f"/api/v1/tasks/{task_id}", json={"project_id": project2}, headers=headers)

    assert response.status_code == 200
    assert response.json()["project_id"] == project2


def test_update_nonexistent_task_returns_404(client):
    headers = get_token(client)

    response = client.put("/api/v1/tasks/99999", json={"title": "Doesnt matter"}, headers=headers)

    assert response.status_code == 404


def test_update_task_owned_by_other_user_forbidden(client):
    owner_headers = get_token(client, "owner@test.com")
    other_headers = get_token(client, "other@test.com")

    project_id = create_project(client, owner_headers)

    r = client.post("/api/v1/tasks", json={"title": "Secret", "project_id": project_id}, headers=owner_headers)
    task_id = r.json()["id"]

    response = client.put(f"/api/v1/tasks/{task_id}", json={"title": "Hacked"}, headers=other_headers)

    assert response.status_code == 403


def test_update_task_fails_if_new_project_invalid(client):
    headers = get_token(client)
    project_id = create_project(client, headers)

    r = client.post("/api/v1/tasks", json={"title": "Move me", "project_id": project_id}, headers=headers)
    task_id = r.json()["id"]

    response = client.put(f"/api/v1/tasks/{task_id}", json={"project_id": 99999}, headers=headers)

    assert response.status_code == 404


#
# DELETE
#

def test_delete_task_success(client):
    headers = get_token(client)
    project_id = create_project(client, headers)

    r = client.post("/api/v1/tasks", json={"title": "Remove", "project_id": project_id}, headers=headers)
    task_id = r.json()["id"]

    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 204

    r2 = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert r2.status_code == 404


def test_delete_nonexistent_task_returns_404(client):
    headers = get_token(client)

    response = client.delete("/api/v1/tasks/99999", headers=headers)

    assert response.status_code == 404


def test_delete_task_owned_by_other_user_forbidden(client):
    owner_headers = get_token(client, "owner@test.com")
    other_headers = get_token(client, "other@test.com")

    project_id = create_project(client, owner_headers)

    r = client.post("/api/v1/tasks", json={"title": "Secret Delete", "project_id": project_id}, headers=owner_headers)
    task_id = r.json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}", headers=other_headers)

    assert response.status_code == 403
