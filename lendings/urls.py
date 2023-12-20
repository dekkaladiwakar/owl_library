from django.urls import path
from .views import (
    ReborrowingEligibilityAPIView,
    BorrowBookAPIView,
    ReturnBookAPIView,
    GetActiveBorrowedBooksAPIView,
    GetAllBorrowedBooksAPIView
)

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
    ),
    path(
        'return/',
        ReturnBookAPIView.as_view(),
        name='return_book'
    ),
    path(
        'borrow/user/<str:user_id>/active',
        GetActiveBorrowedBooksAPIView.as_view(),
        name='get_active_borrowed_books'
    ),
    path(
        'borrow/user/<str:user_id>/all',
        GetAllBorrowedBooksAPIView.as_view(),
        name='get_all_borrowed_books'
    )
]
