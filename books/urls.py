from django.urls import path
from .views import AvailableBooksList
from .views import BooksByAuthorAPIView

urlpatterns = [
    path(
        'available/',
        AvailableBooksList.as_view(),
        name='available_books_list'
    ),
    path(
        'author/<str:author_name>',
        BooksByAuthorAPIView.as_view(),
        name='books_by_author'
    )
]
