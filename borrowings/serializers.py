from rest_framework import serializers
from borrowings.models import Borrowing
from books.models import Book


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ("id", "borrow_date", "actual_return_date", "user")

    def validate(self, data):
        book = data["book"]
        if book.inventory < 1:
            raise serializers.ValidationError("This book is currently not available.")
        return data

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    book_author = serializers.CharField(source="book.author", read_only=True)
    book_cover = serializers.CharField(source="book.cover", read_only=True)
    book_daily_fee = serializers.DecimalField(source="book.daily_fee", max_digits=5, decimal_places=2, read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_email",
            "book",
            "book_title",
            "book_author",
            "book_cover",
            "book_daily_fee",
        ]
