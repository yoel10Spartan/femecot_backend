from django.urls import path

from apps.payments.views import course_payment, create_checkout_session, generate_pdf

urlpatterns = [
    path('', course_payment),
    path('pdf/', generate_pdf),
    path('create_checkout_session/', create_checkout_session),
]