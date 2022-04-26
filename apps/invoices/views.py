from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from apps.invoices.models import Invoice
from apps.invoices.serializers import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer