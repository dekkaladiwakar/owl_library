from django.test import TestCase
from books.models import Book
from authors.models import Author
from django.core.exceptions import ValidationError
from datetime import datetime
import uuid


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_author = Author.objects.create(
            name='Blackbeard', age=35, gender='Male'
        )

        cls.test_book = Book.objects.create(
            owl_id=uuid.uuid4(),
            author=cls.test_author, title='Tale of a Tornado',
            pages=235, type='handmade',
            releasedAt=datetime(2023, 12, 19, 1, 1)
        )

    def test_creation(self):
        self.assertTrue(isinstance(self.test_book, Book))

    def test_title_content(self):
        self.assertEquals(self.test_book.title, 'Tale of a Tornado')

    def test_book_has_correct_author(self):
        self.assertEquals(self.test_book.author, self.test_author)

    def test_pages_number(self):
        self.assertEquals(self.test_book.pages, 235)

    def test_type_content(self):
        self.assertEquals(self.test_book.type, 'handmade')

    def test_is_available_flag(self):
        self.assertTrue(self.test_book.is_available)

    def test_releasedAt_content(self):
        self.assertEquals(
            self.test_book.releasedAt, datetime(2023, 12, 19, 1, 1)
        )

    # To test the unique_together constraint in Book model
    def test_unique_title_for_same_author(self):
        Book.objects.create(
            owl_id=uuid.uuid4(),
            title='A not so Unique name',
            author=self.test_author,
            pages=100,
            type='hardcover',
            releasedAt=datetime.now()
        )
        with self.assertRaises(ValidationError):
            book = Book(title='A not so Unique name', author=self.test_author)

            # This should raise a ValidationError
            # as it check for models field validations
            book.full_clean()

            # This will raise an IntegrityError
            # book.save()

    def test_str_method(self):
        self.assertEquals(str(self.test_book), 'Tale of a Tornado')
