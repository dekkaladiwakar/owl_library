from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from authors.models import Author
from .serializers import BookSerializer


# Book CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class AvailableBooksList(APIView):
    def get(self, request):
        books = Book.objects.filter(is_available=True)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BooksByAuthorAPIView(APIView):
    def get(self, request, author_name):
        try:
            author = Author.objects.get(name=author_name)
            books = Book.objects.filter(author=author)

            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response(
                {"error": "author not found"}, status=status.HTTP_404_NOT_FOUND
            )
