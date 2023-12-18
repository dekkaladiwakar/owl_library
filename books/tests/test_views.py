from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from books.models import Book
from authors.models import Author
from books.serializers import BookSerializer
from datetime import datetime
import uuid


class AvailableBooksListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(name='Charlie')

        cls.test_book_1 = Book.objects.create(
            owl_id=uuid.uuid4(),
            author=test_author, title='Tale of a Tornado- Part 1',
            pages=235,
            type='handmade',
            releasedAt=datetime(2022, 12, 19, 1, 1)
        )

        cls.test_book_2 = Book.objects.create(
            owl_id=uuid.uuid4(),
            author=test_author, title='Tale of a Tornado- Part 2',
            pages=235,
            type='paperback',
            releasedAt=datetime(2023, 12, 19, 1, 1)
        )

    def setUp(self):
        self.client = APIClient()

    def test_get_available_books(self):
        response = self.client.get(reverse('available_books_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = BookSerializer(
            [
                self.test_book_1,
                self.test_book_2
            ],
            many=True).data

        response_data = response.data

        self.assertEqual(response_data, expected_data)
