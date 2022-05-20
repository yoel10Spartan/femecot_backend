from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.bursary.models import Bursary
from apps.invoices.models import Invoice
from apps.invoices.serializers import InvoiceSerializer
from apps.prices.models import Prices

from apps.users.models import Users
from apps.users.serializers import UserSerializer
from datetime import datetime

import qrcode
import os

from django.conf import settings
from django.http import HttpResponse

import xlsxwriter

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
    
class ExcelViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    def list(self, request):
        libro = xlsxwriter.Workbook('users.xls')
        hoja = libro.add_worksheet()
        
        header = [
            'id', 
            'nombre', 
            'apellidos', 
            'correo electronico',
            'dirección',
            'cp',
            'estado',
            'pais',
            'municipio o alcaldía',
            'telefono',
            'celular',
            'empresa o institución',
            'especialidad',
            'cédula profesional',
            'cédula de especialidad',
            'costo de inscripcción',
            'nombre o razon social',
            'rfc',
            'calle',
            'numero exterior',
            'numero interior',
            'colonia',
            'cp',
            'municipio o alcaldia',
            'estado',
            'correo de facturacion',
            'telefono de facturación',
            'forma de pago',
            'uso de la factura',
            'regime'
        ]
        
        row = 0
        col = 0
        
        for i in header:
            hoja.write(row, col, i)
            col+=1
        
        queryset_update = Users.objects.all()
        
        data = self.serializer_class(queryset_update, many=True)
        
        users_data = []
        
        for i in data.data:
            data_user = []
            for j in i:
                data_user.append(i[j])
                
            invoice_user_id = data_user.pop()
            
            if invoice_user_id:
                invoice = Invoice.objects.filter(pk=invoice_user_id).first()
                invoice_serializer = InvoiceSerializer(invoice)
                
                for i in invoice_serializer.data:
                    data_user.append(invoice_serializer.data[i])
                
            users_data.append(data_user)
            
        row = 1
        col = 0
            
        for _user_data in users_data:
            col = 0
            for i in _user_data:
                hoja.write(row, col, i)
                col+=1
            row+=1
        
        libro.close()
        
        file_path = os.getcwd() + '/users.xls'
        
        with open(file_path, 'rb') as f:
           file_data = f.read()
        
        response = HttpResponse(file_data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=usuarios.xls'

        return response