import pytest
import requests

ENDPOINT = "http://127.0.0.1:8000/"

LOGIN_PAYLOAD = {
    "username": "harshanaik2020@gmail.com",
    "password": "Harshanaik12##"
}

# Login once and retrieve JWT token
login_response = requests.post(
    ENDPOINT + "login",
    data=LOGIN_PAYLOAD
)

assert login_response.status_code == 202

TOKEN = login_response.json()["access_token"]


def get_auth_headers():
    return {
        "Authorization": f"Bearer {TOKEN}"
    }


def test_call_endpoint():
    response = requests.get(ENDPOINT + "posts/")

    assert response.status_code == 200


def test_create_user():
    payload = {
        "user_id": 451,
        "email": "harsh@gmail.com",
        "password": "Harshanaik12##",
        "phone_number": "8494980841"
    }

    response = requests.post(
        ENDPOINT + "user/create_user",
        json=payload
    )

    assert response.status_code == 201

    print(response.json())


def test_login():
    response = requests.post(
        ENDPOINT + "login",
        data=LOGIN_PAYLOAD
    )

    assert response.status_code == 202

    token = response.json()["access_token"]

    assert token is not None
    print(token)


def test_access_posts():
    response = requests.get(
        ENDPOINT + "posts/",
        headers=get_auth_headers()
    )

    assert response.status_code == 200

    print(response.json())


def test_create_update_delete_post():


    # Create Post

    create_payload = {
        "id": 17,
        "title": "My Journey Learning FastAPI",
        "content": (
            "Over the past few weeks I have been learning FastAPI, SQLAlchemy, "
            "PostgreSQL, Alembic migrations, JWT authentication, and automated "
            "API testing with Pytest. Building a complete REST API project has "
            "helped me understand backend development much better."
        )
    }

    create_response = requests.post(
        ENDPOINT + "posts/create_post",
        headers=get_auth_headers(),
        json=create_payload
    )

    assert create_response.status_code == 201, create_response.text

    task_id = create_payload["id"]

    # Verify Created Post
    
    get_response = requests.get(
        ENDPOINT + f"posts/{task_id}",
        headers=get_auth_headers()
    )

    assert get_response.status_code == 200

    post_data = get_response.json()

    assert post_data["id"] == task_id
    assert post_data["title"] == create_payload["title"]
    assert post_data["content"] == create_payload["content"]

    # -----------------------------
    # Update Post

    update_payload = {
        "title": "My Journey Learning FastAPI - Updated",
        "content": (
            "After implementing authentication and authorization, I started "
            "writing integration tests using Pytest. I learned how to test "
            "protected routes, create and update resources, validate responses, "
            "and ensure database consistency. This has significantly improved "
            "the reliability of my API."
        )
    }

    update_response = requests.put(
        ENDPOINT + f"posts/update/{task_id}",
        headers=get_auth_headers(),
        json=update_payload
    )

    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Successfully updated"


    # Verify Updated Post

    get_response = requests.get(
        ENDPOINT + f"posts/{task_id}",
        headers=get_auth_headers()
    )

    updated_post = get_response.json()

    assert updated_post["title"] == update_payload["title"]
    assert updated_post["content"] == update_payload["content"]


    # Delete Post

    delete_response = requests.delete(
        ENDPOINT + f"posts/delete/{task_id}",
        headers=get_auth_headers()
    )

    assert delete_response.status_code == 204

