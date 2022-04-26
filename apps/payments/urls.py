from django.urls import path

from apps.payments.views import course_payment

urlpatterns = [
    path('', course_payment),
]