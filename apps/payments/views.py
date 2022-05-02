import os
from tkinter.messagebox import NO
from unittest import result
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from django.conf import settings

import stripe
from apps.courses.models import CoursesPay

from apps.users.models import Users

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

import qrcode
import qrcode.image.svg
from io import BytesIO

from weasyprint import HTML
# from weasyprint.fonts import FontConfiguration
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import render_to_string


def send_email(email_str: str, context: dict):
    template = get_template('index.html')
    content = template.render(context)
    
    try:
        email = EmailMultiAlternatives(
            'Congreso',
            'Congreso',
            settings.EMAIL_HOST_USER,
            [
                email_str, 
                'femengi@yahoo.com.mx', 
                'contacto@ole-sfera.com'
            ]   
        )
        
        email.attach_alternative(content, 'text/html')
        email.send()
    except:
        print('error')
        raise Response('Error')

@api_view(['POST'])
def course_payment(request):
    user_id = request.data.get('user_id')
    
    user = Users.objects.filter(pk=user_id).first()
    amount = user.price_pay * 100
    
    if amount >= 10:
        id = request.data.get('id')
        description = request.data.get('description')
    
    try:
        
        if amount > 10:
            charge = stripe.Charge.create(
                amount=amount,
                currency="mxn",
                description=description,
                source="tok_visa",
                idempotency_key=id,
                api_key='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'
            )
            # api_key='rk_test_51KqnPcG8JjahQ8bbtZvX1XgrqY8MaqXpiNNB30lxnNUMTWjUIVQ82T4WZePzS8d9BqjnEt3hA1QR5YaE4mvau3MK00Sh6WobP8'
            # api_key='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'
        
        course_pre = user.course_pre
        course_trans = user.course_trans
    
        if course_pre.id == 4:
            four_persons = CoursesPay.objects.filter(id=4).first()
            CoursesPay.objects.filter(id=4).update(persons=four_persons.persons+1)
            
        if course_trans.id == 5:
            five_persons = CoursesPay.objects.filter(id=5).first()
            CoursesPay.objects.filter(id=5).update(persons=five_persons.persons+1)
    
        # 'image': 'http://144.126.210.41/media/{}.jpg'.format(user.id),
        # 'portada': 'http://144.126.210.41/media/portada.jpg'
        
        # 'image': 'http://127.0.0.1:8080/media/{}.jpg'.format(user.id),
        # 'portada': 'http://127.0.0.1:8080/media/portada.jpg'
        
        context = {
            'price_pay': user.price_pay,
            'user': user,
            'image': 'https://www.congreso.icu/media/{}.jpg'.format(user.id),
            'portada': 'https://www.congreso.icu/media/portada.jpg'
        }
        
        send_email(user.email, context)
        
        return Response({'ok': True})
    except stripe.error.StripeError as e:
        raise Response({'ok': False})

def link_callback(uri, rel):
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

@api_view(['POST'])
def generate_pdf(request):
    user_id = request.data['user_id']
    
    user = Users.objects.filter(pk=user_id).first()
    
    # 'image': 'http://144.126.210.41/media/{}.jpg'.format(user.id),
    #     'portada': 'http://144.126.210.41/media/portada.jpg'
    
    # 'image': 'http://127.0.0.1:8080/media/{}.jpg'.format(user.id),
    # 'portada': 'http://127.0.0.1:8080/media/portada.jpg'
    
    context = {
        'price_pay': user.price_pay,
        'user': user,
        'image': 'https://www.congreso.icu/media/{}.jpg'.format(user.id),
        'portada': 'https://www.congreso.icu/media/portada.jpg'
    }
    
    template = get_template('index.html')
    html = template.render(context) 
    
    file = open(os.path.join(settings.MEDIA_ROOT, '{}.pdf'.format(user.id)), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file, link_callback=link_callback)
    file.seek(0)
    pdf = file.read()
    file.close ()
    
    # 'link': 'http://127.0.0.1:8080/media/{}.pdf'.format(user.id)
    # 'link': 'http://144.126.210.41/media/{}.pdf'.format(user.id)
    
    return Response({
        'link': 'https://www.congreso.icu/media/{}.pdf'.format(user.id)
    })
    
# <img class="qr" src="https://qrcode.tec-it.com/API/QRCode?data=smsto%3A555-555-5555%3AGenerador+de+C%C3%B3digos+QR+de+TEC-IT" alt="qr">
# <div style="margin: auto">
#     {{ svg|safe }}
# </div>
# <img class="qr" src={{ image }} alt="qr">