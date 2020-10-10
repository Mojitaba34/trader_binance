from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gateway.models import User
from django.views import View

from gateway.api.serializers import UserRegisterSerializer

from rest_framework.authtoken.models import Token

from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import email_token

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import smtplib


"""
Registration part That Contains email sending process and make Validation link for user
"""
@api_view(['POST',])
def register(request):

    if request.method =='POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['responce'] = 'Done!!'
            data['Email'] = user.email
            data['UserName'] = user.username
            token = Token.objects.get(user = user).key
            data['Token'] = token

            # Sending Email Part
            username = request.POST.get('username')
            user = User.objects.get(username__exact=username)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            sending_userGmail_address = ''
            gmail_password = ''
            server.login(sending_userGmail_address,gmail_password)
            # Validation link Create
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('gateway:verification_account',kwargs={'uid':uid,'token':email_token.make_token(user)})

            active_url = 'http://'+ domain + link
            # Email Title and body to Send
            subject = 'Email verification'
            body = 'Hi Please use this link to activate your account\n'+active_url

            Massage = f'Subject:{subject}\n\n{body}'

            server.sendmail(
                f'{sending_userGmail_address}',
                f'{user.email}',
                Massage
            )
            server.quit()
            return Response("Please Check Your email")
        else:
            data = serializer.errors
            return Response(data)

       


"""
This is Class base view 
Checks for Validation link and Activate The Account
"""

class Verification(View):

    def get(self, request, uid, token):
        try:
            user_id = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            if not email_token.check_token(user,token):
                return HttpResponse('The link is invalid')

            if user.is_active:
                return HttpResponse("Your account is active")
            user.is_active = True
            user.save()
            return HttpResponse("Your account Is now active")
        except Exception as e:
            pass
        return HttpResponse("Ok")


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


"""
The CustomAuthToken is Class That contains The Custom authtication 
And Also Acts Like Login process
"""
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try: 
            User.objects.get(username__exact=request.data['username'])
        except User.DoesNotExist:
            return Response("Username Dose Not exists")
        try:
            user = User.objects.get(username__exact=request.data['username'])
            if not user.is_active:
                return Response('Please activate Your account First')
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
        except:
            return Response("Please Check You username Or Password")
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
