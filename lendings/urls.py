from django.urls import path
from .views import ReborrowingEligibilityAPIView

urlpatterns = [
    path(
        'eligible/book/<str:owl_id>/user/<str:user_id>/',
        ReborrowingEligibilityAPIView.as_view(),
        name='reborrowing_eligibility'
    )
]
