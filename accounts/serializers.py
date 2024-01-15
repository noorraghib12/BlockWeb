from rest_framework.response import Response
from django.db.models import Q
from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import auth
from .emails import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['email','is_active']


class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Profile
        fields='__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    profile= ProfileSerializer(read_only=True)
    class Meta:
        model=User
        fields=('email','is_active','profile')

class ForgotPassEmail(serializers.Serializer):
    email=serializers.EmailField()

class ForgotPassVerify(serializers.Serializer):
    email=serializers.EmailField()
    password_init=serializers.CharField()
    password_confirm=serializers.CharField()
    forgot_pass_token=serializers.CharField()

    def validate(self,data):
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Incorrect Email. No user with this email exists in database")
        elif data['password_init']!=data['password_confirm']:
            raise serializers.ValidationError("Password and Password confirmation doesnt match.")
        else:
            return data
    


class RegisterSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password_init=serializers.CharField(max_length=200,write_only=True)
    password_confirm=serializers.CharField(max_length=200,write_only=True)
    is_active=serializers.BooleanField(default=False)
    def validate(self,data):
        print(data)
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("There is already a user with the current email/username within the database. Please use a different username/email")
        elif data['password_init']!=data['password_confirm']:
            raise serializers.ValidationError("Password and Password confirmation doesnt match.")
        else:
            return data
        
    def create(self,validated_data):
        validated_data['password']=validated_data['password_confirm']
        user=User.objects.create_user(
            password=validated_data['password_confirm'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            )
        return user
        

class VerifyRegistration(serializers.ModelSerializer):
    class Meta:
        model=User 
        fields=['email','email_verify_token','is_active']
    def validate(self,data):
        user=User.objects.filter(email=data['email'])
        if not user.exists():
            return {'message':'User doesnt exist in database with provided email address'}
        elif user.first().email_verify_token!=data['email_verify_token']:
            return {'message':f'Incorrect UUID token has been provided for activiting account with email:{user.email}'}    
        return data
    
    def update(self,instance,validated_data):
        instance.email=validated_data.get('email',instance.email)
        instance.email_verify_token=validated_data.get('email_verify_token', instance.email_verify_token)
        instance.is_active=True
        instance.save()
        return instance



            
            


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()


    def validate(self,instance,data):
        if not instance:
            raise serializers.ValidationError(f"Sorry, user with Email:{data['email']} doesnt exist")        
        elif not instance.is_active:
            raise serializers.ValidationError(f"Sorry user with Email: {data['email']} hasn't been activated yet. Please use UUIID sent to registered email for verifying and activating account")
        else:
            return data
        
    def get_jwt_token(self,data):
        user=auth.authenticate(username=data['username'],password=data['password'])
        if not user:
            return {'message': "Invalid Credentials"}
        refresh=RefreshToken.for_user(user)
        return  {
            'messsage':'Loginmusic Success!',
            'data':{
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                }
            }
    