from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from django.conf import settings

import stripe

from apps.users.models import Users

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

def send_email(email: str, context: dict):
    template = get_template('index.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'Congreso',
        settings.EMAIL_HOST_USER,
        [email]   
    )
    
    email.attach_alternative(content, 'text/html')
    email.send()

@api_view(['POST'])
def course_payment(request):
    user_id = request.data['user_id']
    id = request.data['id']
    description = request.data['description']
    
    user = Users.objects.filter(pk=user_id).first()
    amount = user.price_pay * 100
    
    try:

        charge = stripe.Charge.create(
            amount=amount,
            currency="mxn",
            description=description,
            source="tok_visa",
            idempotency_key=id,
            api_key='rk_test_51KqnPcG8JjahQ8bbtZvX1XgrqY8MaqXpiNNB30lxnNUMTWjUIVQ82T4WZePzS8d9BqjnEt3hA1QR5YaE4mvau3MK00Sh6WobP8'
        )
        
        context = {
            'price_pay': user.price_pay,
            'user': user
        }
        
        send_email(user.email, context)
        
        return Response({'ok': True})
    except stripe.error.StripeError as e:
        return Response({'ok': False})
    
    