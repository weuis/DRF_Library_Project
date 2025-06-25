from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["daily_fee"] = f"${rep['daily_fee']}"
        return rep