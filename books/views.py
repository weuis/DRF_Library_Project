from rest_framework import viewsets, filters, status
from books.models import Book
from books.serializers import BookSerializer

from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = {
        "daily_fee": ["gte", "lte"],
        "inventory": ["gte", "lte"],
    }
    search_fields = ["title", "author"]
    ordering_fields = ["title", "daily_fee", "inventory"]
    ordering = ["title"]

    @action(detail=True, methods=["post"])
    def borrow(self, request, pk=None):
        book = self.get_object()
        if book.inventory <= 0:
            return Response({"error": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)
        book.inventory -= 1
        book.save()
        return Response({"message": "Book borrowed successfully."})