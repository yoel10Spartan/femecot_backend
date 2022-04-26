from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from apps.users.models import Users
from apps.users.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer