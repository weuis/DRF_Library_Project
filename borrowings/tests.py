import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from borrowings.models import Borrowing
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="user@example.com",
        password="Password123!",
        first_name="John",
        last_name="Doe",
    )


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        email="staff@example.com",
        password="Password123!",
        first_name="Staff",
        last_name="User",
        is_staff=True,
    )


@pytest.fixture
def book():
    return Book.objects.create(
        title="Sample Book",
        author="Author A",
        cover="SOFT",
        inventory=3,
        daily_fee=1.50,
    )


@pytest.mark.django_db
def test_create_borrowing_decrements_inventory(api_client, user, book):
    api_client.force_authenticate(user=user)
    url = reverse("borrowing-list")

    data = {
        "book": book.id,
        "expected_return_date": (date.today() + timedelta(days=7)).isoformat(),
    }

    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    book.refresh_from_db()
    assert book.inventory == 2

    borrowing = Borrowing.objects.get(id=response.data["id"])
    assert borrowing.user == user
    assert borrowing.book == book


@pytest.mark.django_db
def test_create_borrowing_fails_if_no_inventory(api_client, user, book):
    book.inventory = 0
    book.save()

    api_client.force_authenticate(user=user)
    url = reverse("borrowing-list")
    data = {
        "book": book.id,
        "expected_return_date": (date.today() + timedelta(days=7)).isoformat(),
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not available" in str(response.data).lower()


@pytest.mark.django_db
def test_list_borrowings_filters_by_user_and_active(api_client, user, staff_user, book):
    Borrowing.objects.create(
        user=user,
        book=book,
        expected_return_date=date.today() + timedelta(days=7),
        actual_return_date=None,
    )
    Borrowing.objects.create(
        user=staff_user,
        book=book,
        expected_return_date=date.today() + timedelta(days=7),
        actual_return_date=date.today(),
    )

    api_client.force_authenticate(user=user)
    url = reverse("borrowing-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    for b in response.data["results"]:
        assert b["user_email"] == user.email

    response = api_client.get(url + "?is_active=true")
    assert all(b["actual_return_date"] is None for b in response.data["results"])

    response = api_client.get(url + "?is_active=false")
    assert all(b["actual_return_date"] is not None for b in response.data["results"])


@pytest.mark.django_db
def test_retrieve_borrowing_detail(api_client, user, book):
    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        expected_return_date=date.today() + timedelta(days=7),
    )
    api_client.force_authenticate(user=user)
    url = reverse("borrowing-detail", args=[borrowing.id])

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user_email"] == user.email
    assert response.data["book_title"] == book.title


@pytest.mark.django_db
def test_return_borrowing(api_client, user, book):
    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        expected_return_date=date.today() + timedelta(days=7),
    )
    api_client.force_authenticate(user=user)
    url = reverse("borrowing-return-borrowing", args=[borrowing.id])

    response = api_client.post(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "successfully returned" in response.data["detail"].lower()

    borrowing.refresh_from_db()
    book.refresh_from_db()
    assert borrowing.actual_return_date == borrowing.expected_return_date
    assert book.inventory == 4

    response = api_client.post(url, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already returned" in response.data["detail"].lower()

