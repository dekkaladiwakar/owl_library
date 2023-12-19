from rest_framework.viewsets import ModelViewSet
from .serializers import AuthorSerializer
from .models import Author


# Author CRUD Operations
class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
