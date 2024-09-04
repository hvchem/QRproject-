from ast import Delete
from io import BytesIO
from django.db import transaction
from django.core.files import File
import os
from django.core.validators import EmailValidator
from urllib import response
from django.http import JsonResponse
import qrcode
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.forms import ValidationError
from QRproject import settings
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view,permission_classes
from rest_framework.generics import (CreateAPIView,)
from rest_framework.permissions import (AllowAny,IsAuthenticated)
from .serializers import ProfieSerializer, QRcodeSerializer, Signupserializer,Userserializer
from . import models 
from .models import QRcode, QRstatus, User,UserManager
from hitcount.views import HitCountMixin
from hitcount.models import HitCount
from django.conf import settings
# Create your views 

#class create_user(CreateAPIView):
#    serializer_class = Signupserializer
#    permission_classes = [AllowAny,]
#sign in api        
@api_view(['POST'])
def create_user(request):
    data = request.data
    
    try:
        EmailValidator(data['email'])
    except  ValidationError : 
        return Response({'details ': 'Invalid email format'} , status = status.HTTP_400_BAD_REQUEST)
            
    user = Signupserializer(data = data)
    
    if user.is_valid() :
        if not User.objects.filter(email = data['email']).exists() :
            user = User.objects.create(        
            email = data['email'],
            password = make_password(data['password']),
            first_name = data['first_name'],
            last_name = data['last_name']
        )
            return Response({'details':'Your account registered successfully'},
                            status=status.HTTP_201_CREATED)
        else :
            return Response({'details': 'the email you entered already exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        
    else : return Response( user.errors ,status=status.HTTP_400_BAD_REQUEST)
        
#user data api        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = Userserializer(request.user)
    return Response(user.data)
# update user data api
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data 
    #email_validator = EmailValidator()
    #try : 
    #    email_validator(data["email"]) 
    #except  ValidationError :
    #    return Response({'details':'Invalid Email format'}, status = status.HTTP_400_BAD_REQUEST)
    
    
    #if  User.objects.filter(email = data["email"]).exclude(pk=user.pk).exists():
    #    return Response({'details':'Email Already used ' }, status = status.HTTP_400_BAD_REQUEST)
    #else :
    #    user.user_name = data["email"]
    #    user.email = data["email"]
        
    if data["password"] != ""  :
        if len(data["password"]) >= 10 :  
            user.password = make_password(data["password"])
        else : 
            return Response({'details':'password must be at least 10 characters '}, status= status.HTTP_400_BAD_REQUEST)
    
    
    serializer = Userserializer(user,data=data,partial=True)
    
    if serializer.is_valid() :
        user.save()
        return Response(serializer.data)
    else :
        return Response(serializer.error)
# delete user api (not completed)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    data=request.data
#user api profile    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_user(request):
    user = ProfieSerializer(request.user)
    return Response(user.data)

#user profile data  updste 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Update_profile(request):
    user = request.user
    data = request.data 
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.image = data["image"]
    
    user.save()
    
    serializer = ProfieSerializer(user,many=False)
    return Response(serializer.data) 


#get qr link api

#def create_qr_row(request):
    
    
 #   page_url = request.data.get("page")
  #  if not page_url:
   #     return Response({"error": "page is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    #with transaction.atomic():
     #   qr_status, created = QRstatus.objects.get_or_create(views=0)
    #qr_code = QRcode.objects.create(   
     #   user = request.user,
      #  title = request.data.get("title"),
     #   page = page_url,
     #   QRstatus = qr_status
    #)
    
    #qr_code.save()
    #return Response({"message": "QR code Row has been created successfully","qr code data ": qr_code.page  }, status=status.HTTP_201_CREATED)

#update qr code page's  link 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_qr_code(request,pk) :

    qrcode = get_object_or_404(QRcode,id=pk)
    
    
    if qrcode.user != request.user :
        return Response({"error":"sorry you can not update this QRcode"}) 

    qrcode.page = request.data.get("page")
    qrcode.title = request.data.get("title")
    if not qrcode.page:
        return Response({"error": "page is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    qrcode.save()
    
    return Response({"message": "QR code Row has been updated successfully","qr code data ": qrcode.page  }, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_QRs(request):
    user = request.user 
    qrcodes = QRcode.objects.filter(user=user)
    
    qr_codes_data= []
    
    for qr_code in qrcodes : 
        qr_codes_data.append({
            'id' : qr_code.id,
            'title' : qr_code.title,
            'page' : qr_code.page,
            'url' : qr_code.url,
            'status' : qr_code.QRstatus.views,
        })
    return Response({'user': user.email, 'qr_codes': qr_codes_data})
# count  the viewrs 
@api_view(['GET'])
def qr_views_and_redirect(request, pk):
    qrcode = get_object_or_404(QRcode, id=pk)
    
    qrcode.QRstatus.views += 1
    qrcode.QRstatus.save()
    
    return redirect(qrcode.page)

    

#generate qr code and its link api  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_qr_code(request):
    page_url = request.data.get("page")
    if not page_url:
        return Response({"error": "page is required"}, status=status.HTTP_400_BAD_REQUEST)
    elif  not (page_url.startswith('https://') or page_url.startswith('http://')):
        return Response({"error": " the link must start with http://"}, status=status.HTTP_400_BAD_REQUEST)
    with transaction.atomic():
        qr_status, created = QRstatus.objects.get_or_create(views=0)
    qr_code = QRcode.objects.create(   
        user = request.user,
        title = request.data.get("title"),
        page = page_url,
        QRstatus = qr_status
        
    )
    
    qr_code.save()
    QR = get_object_or_404(QRcode, id = qr_code.id)
    # qr_content = get_random_string(length=32)
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L ,
        box_size= 10,
        border =  4,
    )
    
    qr.add_data(f"http://{settings.LOCALHOST}:8000/api/{str(QR.id)}")
    #qr.add_data(str(QR.page))
    qr.make(fit=True)
    
    img = qr.make_image(fill='black' , back_color='white')
    
    buffer = BytesIO()
    img.save(buffer , format="PNG")
    buffer.seek(0)
    
    
    file_name = f"{get_random_string(length=10)}.png"
    file_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', file_name)
    
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'wb') as f:
        f.write(buffer.getvalue())
        
    qr_code_url = os.path.join(settings.MEDIA_URL, 'qr_codes' , file_name)
    
    
    qr_code.url = qr_code_url
    
    qr_code.save()
    
    #/qr_code_image = ContentFile(buffer.getvalue())
    #/qr_code.url.save(file_name, qr_code_image)
    
    
    return Response({"message": "QR code generated successfully", "qr_code_url": qr_code.url}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_QR(request,pk) :
    qr = get_object_or_404(QRcode,id=pk)
    if qr.user != request.user :
        return Response({"error":"Sorry you can't delete this product"},
                        status = status.HTTP_403_FORBIDDEN)
    
    qr.delete()
    return Response({"Details":"Delete action is done "},
                        status = status.HTTP_200_OK)

