from django.urls import path
from rest_framework import routers
from apps.users.views import UserViewSet

router = routers.SimpleRouter()

router.register(r'users', UserViewSet)

urlpatterns = router.urls