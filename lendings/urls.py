from django.urls import path
from .views import ReborrowingEligibilityAPIView, BorrowBookAPIView

urlpatterns = [
    path(
        'eligible/book/<str:owl_id>/user/<str:user_id>/',
        ReborrowingEligibilityAPIView.as_view(),
        name='reborrowing_eligibility'
    ),
    path(
        'borrow/',
        BorrowBookAPIView.as_view(),
        name='borrow_book'
    )
]
