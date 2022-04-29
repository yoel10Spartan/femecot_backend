from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from apps.invoices.models import Invoice
from apps.invoices.serializers import InvoiceSerializer
from apps.users.models import Users

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    
    def setInstance(self, user_id, id_invoice):
        data = Invoice.objects.filter(id=id_invoice).first()
        Users.objects.filter(pk=user_id).update(invoice=data)
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        data = super().create(request, args, kwargs)
        
        id = data.data['id']
        
        self.setInstance(user_id, id)
        
        return data