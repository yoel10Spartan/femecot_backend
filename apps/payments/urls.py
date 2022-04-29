from django.urls import path

from apps.payments.views import course_payment, generate_pdf

urlpatterns = [
    path('', course_payment),
    path('pdf/', generate_pdf),
]