from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lending
from books.models import Book
from django.utils import timezone
from datetime import timedelta


class ReborrowingEligibilityAPIView(APIView):
    def get(self, request, owl_id, user_id):
        try:
            book = Book.objects.get(owl_id=owl_id)
            latest_lending = Lending.objects.filter(
                user_id=user_id, book=book).order_by('-borrowedAt').first()

            if not latest_lending:
                return Response({'eligible': True})

            is_special_author = book.author.name.startswith('J')

            # Add these values as normal_author_th and special_author_th in ENV
            # th- threshold
            three_months = timedelta(days=90)
            six_months = timedelta(days=180)

            threshold_date = latest_lending.borrowedAt + \
                (six_months if is_special_author else three_months)

            if timezone.now() >= threshold_date:
                return Response({'eligible': True})
            else:
                return Response({
                    'eligible': False,
                    'eligible_from': threshold_date.isoformat()
                })

        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )
