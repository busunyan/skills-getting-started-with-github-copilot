from src.app import activities


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_succeeds_when_spot_available(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up new.student@mergington.edu for Chess Club"
    assert "new.student@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_returns_400_when_activity_is_full(client):
    activities["Chess Club"]["max_participants"] = len(activities["Chess Club"]["participants"])

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_does_not_add_participant_when_full(client):
    activities["Chess Club"]["max_participants"] = len(activities["Chess Club"]["participants"])

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "full-case@mergington.edu"},
    )

    assert response.status_code == 400
    assert "full-case@mergington.edu" not in activities["Chess Club"]["participants"]


def test_signup_duplicate_email_returns_400_even_if_full(client):
    existing_email = activities["Chess Club"]["participants"][0]
    activities["Chess Club"]["max_participants"] = len(activities["Chess Club"]["participants"])

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_activity_not_found_returns_404(client):
    response = client.post(
        "/activities/Nonexistent%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_422_when_email_is_missing(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_unregister_succeeds_for_registered_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_unregistered_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_returns_422_when_email_is_missing(client):
    response = client.delete("/activities/Chess%20Club/signup")

    assert response.status_code == 422
