from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    daily_fee_display = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_daily_fee_display(self, obj):
        return f"${obj.daily_fee:.2f}"

    def get_is_available(self, obj):
        return obj.inventory > 0

    def validate_daily_fee(self, value):
        if value < 0:
            raise serializers.ValidationError("Daily fee must be non-negative.")
        return value

    def validate_inventory(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory must be non-negative.")
        return value