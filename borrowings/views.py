from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingDetailSerializer
from books.models import Book


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user").all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user", "actual_return_date"]

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        is_active = self.request.query_params.get("is_active")
        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "false":
            queryset = queryset.filter(actual_return_date__isnull=False)
        return queryset

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date is not None:
            return Response({"detail": "Book already returned."}, status=400)

        borrowing.actual_return_date = request.data.get("actual_return_date") or borrowing.expected_return_date
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response({"detail": "Book successfully returned."})


