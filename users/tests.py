from django.test import TestCase
from .models import User


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(name='John Wick')

    def test_creation(self):
        self.assertTrue(isinstance(self.test_user, User))

    def test_name_content(self):
        self.assertEquals(self.test_user.name, 'John Wick')

    def test_str_method(self):
        self.assertEquals(str(self.test_user), 'John Wick')
