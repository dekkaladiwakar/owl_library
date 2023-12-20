from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from books.models import Book
from authors.models import Author
from books.serializers import BookSerializer
from datetime import datetime
import uuid


# Testcases for book CRUD Operations
class BookViewSetTestCase(APITestCase):

    def setUp(self):
        self.test_author = Author.objects.create(name='Charlie')

        # Test data
        # Didn't include owl_id as it will be created while using Client
        # Using Author ID as the API accepts id instead of an instance
        self.book_data = {
            'title': 'A sniper\'s paradise- Part 2',
            'author': self.test_author.id,
            'pages': 234,
            'type': 'paperback',
            'releasedAt': '2023-08-12T09:10:00Z'
        }

        self.book = Book.objects.create(
            owl_id=uuid.uuid4(),
            title='A sniper\'s paradise',
            author=self.test_author,
            pages=234,
            type='paperback',
            releasedAt=datetime.now()
        )

    def test_get_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), len(response.data))

    def test_create_book(self):
        response = self.client.post(reverse('book-list'), self.book_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        response = self.client.get(
            reverse('book-detail', args=[self.book.owl_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'A sniper\'s paradise')

    def test_patch_book(self):
        update_data = {'title': 'A Sniper\'s paradise'}
        response = self.client.patch(
            reverse('book-detail', args=[self.book.owl_id]), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'A Sniper\'s paradise')

    def test_update_book(self):
        update_data = {
            'title': 'A sniper\'s paradise',
            'author': self.test_author.id,
            'pages': 243,
            'type': 'hardcover',
            'releasedAt': '2022-08-12T09:10:00Z'
        }
        response = self.client.put(
            reverse('book-detail', args=[self.book.owl_id]), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'A sniper\'s paradise')
        self.assertEqual(self.book.author.name, 'Charlie')
        self.assertEqual(self.book.pages, 243)
        self.assertEqual(self.book.type, 'hardcover')

        # As the string doesn't contain tzinfo I'm setting it to None
        # Or you can use 2022-08-12T09:10:00+00:00Z and remove tzinfo
        self.assertEqual(self.book.releasedAt.replace(
            tzinfo=None).isoformat() + 'Z', '2022-08-12T09:10:00Z')

    def test_delete_book(self):
        response = self.client.delete(
            reverse('book-detail', args=[self.book.owl_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


# Testcase for AvailableBooks API
class AvailableBooksListTest(APITestCase):
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


# Testcase for BooksByAuthor API
class BookByAuthorTestCase(APITestCase):
    def setUp(self):
        test_author = Author.objects.create(name='Charlie')

        Book.objects.create(
            owl_id=uuid.uuid4(),
            title='A sniper\'s paradise',
            author=test_author,
            pages=234,
            type='paperback',
            releasedAt=datetime.now()
        )

    def test_books_by_author(self):
        response = self.client.get(
            reverse('books_by_author', args=['Charlie']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('A sniper\'s paradise', response.data[0]['title'])

    def test_author_not_found(self):
        response = self.client.get(
            reverse('books_by_author', args=['Blackbeard']))
        self.assertEqual(response.status_code, 404)
