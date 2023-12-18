from django.urls import path
from .views import AvailableBooksList

urlpatterns = [
    path(
        'available/',
        AvailableBooksList.as_view(),
        name='available_books_list'
    )
]
