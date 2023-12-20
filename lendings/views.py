from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from books.models import Book
from .models import Lending
from django.utils import timezone
from django.db import transaction
from datetime import timedelta, datetime


class BorrowBookAPIView(APIView):
    def post(self, request):
        try:
            owl_id = request.data.get('owl_id')
            user_id = request.data.get('user_id')

            # 1. Check if user exists
            user = User.objects.get(id=user_id)

            # 2. start a transaction and check if the book is available
            with transaction.atomic():
                book = Book.objects.select_for_update().get(owl_id=owl_id)
                if not book.is_available:
                    return Response({
                        'error': 'Book is not available',
                    }, status=status.HTTP_400_BAD_REQUEST)

                # 3. Check if the user is eligible to borrow the book
                eligibility_view = ReborrowingEligibilityAPIView()
                eligibility_response = eligibility_view.get(
                    request, book.owl_id, user.id)

                if not eligibility_response.data['eligible']:
                    return Response(
                        {'error': 'User not eligible to borrow this book'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 4. Record the entry in Lending
                Lending.objects.create(
                    book=book, user=user,
                    borrowedAt=datetime.now(),
                    returnedAt=datetime.now() + timedelta(days=14)
                )

                # 5. Set the book as not available
                book.is_available = False
                book.save()

                return Response(
                    {'message': 'Book borrowed successfully'},
                    status=status.HTTP_200_OK
                )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )


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
