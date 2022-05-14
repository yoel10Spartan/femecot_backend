from django.urls import path

from apps.payments.views import generate_pdf, send_email_user

urlpatterns = [
    # path('', course_payment),
    path('pdf/', generate_pdf),
    # path('create_checkout_session/', create_checkout_session),
    path('send_email/', send_email_user),
]