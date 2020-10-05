from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gateway.models import User

from gateway.api.serializers import UserRegisterSerializer

from rest_framework.authtoken.models import Token

import smtplib

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
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST',])
def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username__exact=username)
            if user.password == password:
                return Response("You have Been Logged in")
            else:
                return Response("Please Check Your Username Or Password")
        except User.DoesNotExist as e:
            return Response("This username Is not Exist Please Register First")

@api_view(['POST',])
def sendemail(request):
    username = request.POST.get('username')
    user = User.objects.get(username__exact=username)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    gmail_user_address = ''
    gmail_password = ''
    server.login(gmail_user_address,gmail_password)

    subject = 'Email Test From Gatewat'
    body = 'Hellow from Mojtaba On Gateway'

    Massage = f'Subject:{subject}\n\n{body}'

    server.sendmail(
        'mojtabadavi14@gmail.com',
        f'{user.email}',
        Massage
    )
    server.quit()
    return Response("Please Check Your email")



    


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try: 
            User.objects.get(username__exact=request.data['username'])
        except User.DoesNotExist:
            return Response("Username Dose Not exists")
        try:
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
