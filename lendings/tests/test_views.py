from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from lendings.models import Lending
from users.models import User
from authors.models import Author
from books.models import Book
from django.utils import timezone
from datetime import datetime, timedelta
import uuid


# Test Cases:
# 1. With no prior borrowings
# 2. with prior borrowings- Pass
# 3. with prior borrowings- Fail
# 4. special author with prior borrowings- Pass
# 5. special author with prior borrowings- Fail
# 6. Not a valid Book
class ReborrowingEligibilityAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name='John Wick')
        self.author = Author.objects.create(name='Charlie')
        self.special_author = Author.objects.create(name='Jason')
        self.book = Book.objects.create(
            owl_id=uuid.uuid4(),
            author=self.author,
            title='A Sniper\'s paradise',
            pages=247,
            type='papaerback',
            releasedAt=datetime.now()
        )
        self.book_2 = Book.objects.create(
            owl_id=uuid.uuid4(),
            author=self.special_author,
            title='Tale of a Tornado',
            pages=368,
            type='hardcover',
            releasedAt=datetime.now()
        )

        self.three_months = timedelta(days=90)
        self.six_months = timedelta(days=180)

    def test_eligibility_no_prior_borrowing(self):
        response = self.client.get(reverse('reborrowing_eligibility', args=[
                                   self.book.owl_id, self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['eligible'], True)

    def test_eligibility_with_prior_borrowing_pass(self):
        Lending.objects.create(
            book=self.book, user=self.user,
            borrowedAt=timezone.now() - self.three_months
        )
        response = self.client.get(reverse('reborrowing_eligibility', args=[
                                   self.book.owl_id, self.user.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['eligible'], True)

    def test_eligibility_with_prior_borrowing_fail(self):
        Lending.objects.create(book=self.book, user=self.user,
                               borrowedAt=timezone.now() - timedelta(days=30))
        response = self.client.get(reverse('reborrowing_eligibility', args=[
                                   self.book.owl_id, self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['eligible'], False)

    def test_special_author_eligibility_with_prior_borrowing_pass(self):
        Lending.objects.create(
            book=self.book_2, user=self.user,
            borrowedAt=timezone.now() - self.six_months
        )
        response = self.client.get(reverse('reborrowing_eligibility', args=[
                                   self.book_2.owl_id, self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['eligible'], True)

    def test_special_author_eligibility_with_prior_borrowing_fail(self):
        Lending.objects.create(
            book=self.book_2, user=self.user,
            borrowedAt=timezone.now() - self.three_months
        )
        response = self.client.get(reverse('reborrowing_eligibility', args=[
                                   self.book_2.owl_id, self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['eligible'], False)

    def test_nonexistent_book(self):
        invalid_uuid_value = uuid.uuid4()
        response = self.client.get(
            reverse('reborrowing_eligibility', args=[
                invalid_uuid_value, self.user.id
            ]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
