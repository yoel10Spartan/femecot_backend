import os
from django.shortcuts import redirect
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

import stripe
# from apps.courses.models import Cours
# esPay

from apps.users.models import Users

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import render_to_string

def send_email(email_str: str, context: dict):
    try:
        template = get_template('index.html')
        
        content = template.render(context)
        
        email = EmailMultiAlternatives(
            'FEMECOT',
            'FEMECOT',
            settings.EMAIL_HOST_USER,
            [
                email_str,
                # 'femengi@yahoo.com.mx',
                # 'contacto@ole-sfera.com',
                # 'franco@ole-sfera.com'
                'munozzecuayoel@gmail.com',
            ]
        )
        email.attach_alternative(content, 'text/html')
        email.send()
    except:
        print('error')
        raise Response('Error')
    
@api_view(['POST'])
def send_email_user(request):
    user_id = request.data['user_id']
    user = Users.objects.filter(pk=user_id).first()

    context = {
        'price_pay': user.price_pay,
        'user': user,
        'image': 'https://congreso.icu/media/{}.jpg'.format(user.id),
        'portada': 'https://congreso.icu/media/portada_photo.jpg'
    }
    
    send_email(user.email, context)
    
    return Response({'ok': True})

def link_callback(uri, rel):
    sUrl = settings.STATIC_URL      
    sRoot = settings.STATIC_ROOT    
    mUrl = settings.MEDIA_URL       
    mRoot = settings.MEDIA_ROOT  
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

    # 'image': 'https://www.congreso.icu/media/{}.jpg'.format(user.id),
    #     'portada': 'https://www.congreso.icu/media/portada.jpg'

    context = {
        'price_pay': user.price_pay,
        'user': user,
        'image': 'http://127.0.0.1:8080/media/{}.jpg'.format(user.id),
        'portada': 'http://127.0.0.1:8080/media/portada.jpg'
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

    # 'link': 'https://www.congreso.icu/media/{}.pdf'.format(user.id)

    return Response({
        'link': 'http://127.0.0.1:8080/media/{}.pdf'.format(user.id)
    })