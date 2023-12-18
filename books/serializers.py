from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'owl_id', 'title', 'author', 'is_available',
            'type', 'pages', 'releasedAt'
        ]
