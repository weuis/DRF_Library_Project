from rest_framework.routers import DefaultRouter
from borrowings.views import BorrowingViewSet
from django.urls import path, include

router = DefaultRouter()
router.register("", BorrowingViewSet, basename="borrowing")

urlpatterns = [
    path("", include(router.urls)),
]