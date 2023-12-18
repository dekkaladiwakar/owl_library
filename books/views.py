from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


class AvailableBooksList(APIView):
    def get(self, request):
        books = Book.objects.filter(is_available=True)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
