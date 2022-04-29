from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from apps.users.models import Users
from apps.users.serializers import UserSerializer

import qrcode
import os

from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        data = super().create(request, args, kwargs)
        
        id = data.data['id']
        name = '{}.jpg'.format(id)
        
        img = qrcode.make(str(id))
        file = open(os.path.join(settings.BASE_DIR, 'media', name), "wb")
        img.save(file)
        file.close()
        
        return data