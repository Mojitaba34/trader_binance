from django.urls import path
from gateway.api.views import (
    register,
    loginUser,
    sendemail
)
# from rest_framework.authtoken.views import obtain_auth_token
from gateway.api.views import CustomAuthToken


app_name = 'gateway'


urlpatterns = [
    path('register', register,name='register'),
    path('login',CustomAuthToken.as_view(),name='Login'),
    path('sendemail',sendemail,name='sendemail')

]