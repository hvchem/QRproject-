from django.conf import settings
from django.urls import path , include
from .views import create_user, current_user, profile_user,Update_profile, update_qr_code, update_user , generate_qr_code ,qr_views_and_redirect,get_my_QRs ,delete_QR 
from rest_framework.authtoken.views import (obtain_auth_token,)

urlpatterns = [
path('auth/signup',create_user,name='signup'),
path('updateuser/',update_user,name='updateuser'),
#path('login/',obtain_auth_token,name='login')
#path('profile/',current_user,name='profile')
path('profile/',profile_user,name='profile'),
path('profile/updateprofile/',Update_profile,name='updateprofile'),
path('generate_qr_code/', generate_qr_code, name='generate_qr_code'),
path('update_qr_code/<str:pk>/',update_qr_code, name='update_qr_code'),
path('<str:pk>',qr_views_and_redirect, name='increment_viewers_of_qr_code'),
path('qr_code/',get_my_QRs, name='get_my_qrs'),
path('delete_qr/<str:pk>',delete_QR, name='delete_qr'),

#path('create_qr_row/', create_qr_row, name='create_qr_row'),
]
