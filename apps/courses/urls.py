from django.urls import path

from apps.courses.views import buy_courses, payment_course_information

urlpatterns = [
    path('', buy_courses),
    path('payment_course_information/', payment_course_information)
]