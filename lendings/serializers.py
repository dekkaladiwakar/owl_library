from rest_framework import serializers
from .models import Lending


class LendingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    author_name = serializers.CharField(
        source='book.author.name', read_only=True)

    class Meta:
        model = Lending
        fields = [
            'user_name',
            'book_title',
            'author_name',
            'borrowedAt',
            'returnedAt'
        ]
