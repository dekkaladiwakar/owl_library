from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BooksByAuthorAPIView, AvailableBooksList

router = DefaultRouter()
router.register(r'', BookViewSet, basename='book')

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
    ),
    path('', include(router.urls)),
]
