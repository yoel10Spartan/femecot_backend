from django.urls import path
from rest_framework import routers
from apps.invoices.views import InvoiceViewSet

router = routers.SimpleRouter()

router.register(r'invoice', InvoiceViewSet)

urlpatterns = router.urls