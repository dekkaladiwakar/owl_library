from django.test import TestCase
from .models import Author


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_author = Author.objects.create(
            name='Blackbeard', age=35, gender='Male'
        )

    def test_creation(self):
        self.assertTrue(isinstance(self.test_author, Author))

    def test_name_content(self):
        self.assertEquals(self.test_author.name, 'Blackbeard')

    def test_age_content(self):
        self.assertEquals(self.test_author.age, 35)

    def test_gender_content(self):
        self.assertEquals(self.test_author.gender, 'Male')

    def test_str_method(self):
        self.assertEquals(str(self.test_author), 'Blackbeard')
