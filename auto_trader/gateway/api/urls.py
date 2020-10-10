from django.urls import path
from gateway.api.views import (
    register,
    Verification
)

from gateway.api.views import CustomAuthToken


app_name = 'gateway'


urlpatterns = [
    path('register', register,name='register'),
    path('login',CustomAuthToken.as_view(),name='Login'),
    path('verification/<uid>/<token>',Verification.as_view(),name='verification_account')

]