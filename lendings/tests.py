from django.test import TestCase
from users.models import User
from authors.models import Author
from books.models import Book
from .models import Lending
from datetime import datetime, timedelta
import uuid


class LendingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(name='John Wick')
        test_author = Author.objects.create(name='Charlie')

        cls.test_book = Book.objects.create(
            owl_id=uuid.uuid4(), title='A Sniper\'s paradise',
            author=test_author, pages=150, type='papaerback',
            releasedAt=datetime.now()
        )

        cls.test_lending = Lending.objects.create(
            user=cls.test_user,
            book=cls.test_book,
            borrowedAt=datetime(2023, 12, 19, 1, 1),
            returnedAt=datetime(2023, 12, 19, 1, 1) + timedelta(days=14)
        )

    def test_lending_creation(self):
        self.assertTrue(isinstance(self.test_lending, Lending))

    def test_lending_user(self):
        self.assertEquals(self.test_lending.user, self.test_user)

    def test_lending_book(self):
        self.assertEquals(self.test_lending.book, self.test_book)

    def test_lending_dates(self):
        self.assertEquals(
            self.test_lending.borrowedAt, datetime(2023, 12, 19, 1, 1)
        )
        self.assertEquals(
            self.test_lending.returnedAt,
            datetime(2023, 12, 19, 1, 1) + timedelta(days=14)
        )

    def test_str_method(self):
        self.assertEquals(
            str(self.test_lending),
            'John Wick has borrowed A Sniper\'s paradise'
        )
