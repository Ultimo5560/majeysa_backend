from django.urls import path
from .views import CreatePreferenceView, mercado_pago_webhook, SendMailFinishView

urlpatterns = [
    # path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    path('create_preference/', CreatePreferenceView.as_view(), name='create_preference'),
    path('send_mail_finish/', SendMailFinishView.as_view(), name='send_mail_finish'),
    path('mercado-pago-webhook/', mercado_pago_webhook, name='mercado_pago_webhook'),
]
