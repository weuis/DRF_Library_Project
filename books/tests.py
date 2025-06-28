import pytest
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def book():
    return Book.objects.create(
        title="1984",
        author="George Orwell",
        cover=Book.CoverType.HARD,
        inventory=3,
        daily_fee=1.99
    )


def test_book_str_method(book):
    assert str(book) == "1984 by George Orwell"


def test_create_book(api_client):
    response = api_client.post("/api/books/", {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "cover": "SOFT",
        "inventory": 2,
        "daily_fee": "2.50"
    }, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == 1


def test_invalid_daily_fee(api_client):
    response = api_client.post("/api/books/", {
        "title": "Bad Fee",
        "author": "Nobody",
        "cover": "SOFT",
        "inventory": 1,
        "daily_fee": "-5.00"
    }, format="json")
    assert response.status_code == 400
    assert "daily_fee" in response.data


def test_invalid_inventory(api_client):
    response = api_client.post("/api/books/", {
        "title": "Bad Inventory",
        "author": "Nobody",
        "cover": "SOFT",
        "inventory": -1,
        "daily_fee": "1.00"
    }, format="json")
    assert response.status_code == 400
    assert "inventory" in response.data


def test_borrow_success(api_client, book):
    response = api_client.post(f"/api/books/{book.id}/borrow/")
    assert response.status_code == 200
    book.refresh_from_db()
    assert book.inventory == 2


def test_borrow_failure_no_inventory(api_client, book):
    book.inventory = 0
    book.save()

    response = api_client.post(f"/api/books/{book.id}/borrow/")
    assert response.status_code == 400
    assert response.data["error"] == "Book is not available."


def test_list_books(api_client, book):
    response = api_client.get("/api/books/")
    assert response.status_code == 200
    assert len(response.data) >= 1


def test_filter_books_by_fee(api_client, book):
    Book.objects.create(
        title="More Expensive",
        author="Someone Else",
        cover="SOFT",
        inventory=2,
        daily_fee=5.00
    )
    response = api_client.get("/api/books/?daily_fee__lte=2.00")
    assert response.status_code == 200
    results = response.data["results"]
    assert all(float(book["daily_fee"]) <= 2.00 for book in results)


def test_search_books(api_client, book):
    response = api_client.get("/api/books/?search=Orwell")
    assert response.status_code == 200
    results = response.data.get("results", response.data)
    assert any("Orwell" in b["author"] for b in results)

