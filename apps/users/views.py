from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.bursary.models import Bursary
from apps.invoices.models import Invoice
from apps.prices.models import Prices

from apps.users.models import Users
from apps.users.serializers import UserSerializer
from datetime import datetime

import qrcode
import os

from django.conf import settings

def create_qr(text, name):
    img = qrcode.make(text)
    file = open(os.path.join(settings.BASE_DIR, 'media', name), "wb")
    img.save(file)
    file.close()

def calc_price(id_price):
    price = Prices.objects.filter(pk=id_price).first()
    data_valid = datetime.fromisoformat(str(price.valid))
    date_now = datetime.now()
    return price.price if data_valid > date_now else price.future_price

def create_invoice(data, id_user): 
    new_invoice = Invoice.objects.create(**data)
    user = Users.objects.filter(pk=id_user)
    user.update(invoice=new_invoice)
    return

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        
        data = super().create(request, args, kwargs)
        
        id = data.data['id']
        name = '{}.jpg'.format(id)
        create_qr(str(id), name)
        
        request.data['id'] = id
        price = calc_price(request.data['price'])
        
        data_invoice = request.data['invoice_data']
        
        if data_invoice:
            create_invoice(request.data['invoice_data'], id)
        
        user = Users.objects.filter(pk=id)
        user.update(price_pay=price)
        user_serializer = UserSerializer(user.first())
        
        return Response(user_serializer.data, status=status.HTTP_200_OK)