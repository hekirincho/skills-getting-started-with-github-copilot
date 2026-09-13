def test_root_redirect(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Verify side effect via GET /activities
    get_response = client.get("/activities")
    assert email in get_response.json()[activity_name]["participants"]


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "Non Existent Club"
    email = "student@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    # Verify side effect via GET /activities
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    # Arrange
    activity_name = "Non Existent Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_enrolled(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notenrolled@mergington.edu"
    url = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
