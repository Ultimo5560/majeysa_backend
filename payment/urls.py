from django.urls import path
from .views import ProcessPaymentView, CreatePreferenceView

urlpatterns = [
    path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    path('create_preference/', CreatePreferenceView.as_view(), name='create_preference'),
]
