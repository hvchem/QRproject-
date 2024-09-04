from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from . import models

User = get_user_model()

class Userserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name','last_name','email','date_joined')
        extra_kwargs = {
            'email':{'read_only':True},
            'password':{'required':True,'allow_blank':False , 'min_length':10 , 'write_only':True}
        }
        
        
        
class Signupserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        extra_kwargs = {
            'first_name':{'required':True,'allow_blank':False},
            'last_name':{'required':True,'allow_blank':False},
            'email':{'required':True,'allow_blank':False},
            'password':{'required':True,'allow_blank':False , 'min_length':10 , 'write_only':True}
        }
        
class ProfieSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['first_name','last_name','password','email','date_joined','image'] 
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True}
}
        
    #def create(self, validated_data):
    #    user = User.objects.create_user(email=validated_data['email'], password=make_password(validated_data['password']),first_name=validated_data['first_name'],last_name=validated_data['last_name'])
    #    return user
    
    
class QRcodeSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.QRcode
        fields = ['URL','page','QRstatus','user','title']
        extra_kwargs = {
            'QRstatus':{'read_only':True},
            
        }
        
        