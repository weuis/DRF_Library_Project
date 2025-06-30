import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="StrongPass123!",
        first_name="Test",
        last_name="User"
    )

@pytest.mark.django_db
def test_register_user_success(api_client):
    url = reverse("user-register")
    data = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "StrongPass123!",
        "password2": "StrongPass123!",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="newuser@example.com").exists()
    user = User.objects.get(email="newuser@example.com")
    assert user.first_name == "New"

@pytest.mark.django_db
def test_register_user_password_mismatch(api_client):
    url = reverse("user-register")
    data = {
        "email": "fail@example.com",
        "first_name": "Fail",
        "last_name": "User",
        "password": "password1",
        "password2": "password2",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data

@pytest.mark.django_db
def test_register_user_duplicate_email(api_client, user):
    url = reverse("user-register")
    data = {
        "email": user.email,
        "first_name": "Dup",
        "last_name": "User",
        "password": "StrongPass123!",
        "password2": "StrongPass123!",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data

@pytest.mark.django_db
def test_user_me_retrieve(api_client, user):
    url = reverse("user-me")
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert response.data["first_name"] == user.first_name

@pytest.mark.django_db
def test_user_me_update(api_client, user):
    url = reverse("user-me")
    api_client.force_authenticate(user=user)
    data = {"first_name": "Updated", "last_name": "Name"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == "Updated"
    assert user.last_name == "Name"

