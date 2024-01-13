
from django.db.models import Q
from models import *
from rest_framework import serializers
from rest_framework_simplejwt import RefreshToken
from django.contrib.auth.models import auth
from emails import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username','email','is_active']


class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=200)
    email=serializers.EmailField()
    password_init=serializers.CharField()
    password_confirm=serializers.CharField()
    is_active=serializers.BooleanField(default=False)
    def validate(self,data):
        if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
            raise serializers.ValidationError("There is already a user with the current email/username within the database. Please use a different username/email")
        elif data['password_init']!=data['password_confirm']:
            raise serializers.ValidationError("Password and Password confirmation doesnt match.")
        else:
            return data
        
    def create(self,validated_data):
        validated_data['password']=validated_data['passowrd_confirm']
        try:
            user=User.objects.create_user(**validated_data)
        except:
            del validated_data['password_init'], validated_data['password_cofirm']
            user=User.objects.create_user(**validated_data)
        user.save()
        send_uuid_email(user.email)
        return validated_data


class VerifyRegistration(serializers.Serializer):
    user_email=serializers.EmailField()
    auth_string=serializers.CharField()
    
    def validate(self,data):
        user=User.objects.filter(email=data['user_email'])
        if not user.exists():
            return {'message':'User doesnt exist in database with provided email address'}
        elif user.email_verify_token!=data['email_verify_token']:
            return {'message':f'Incorrect UUID token has been provided for activiting account with email:{user.email}'}    
        return data


            
            


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()


    def validate(self,data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(f"Sorry, user with username:{data['username']} doesnt exist")        
        elif not User.objects.filter(username=data['username'])[0].is_active:
            raise serializers.ValidationError(f"Sorry user {data['username']} hasn't been activated yet. Please use UUIID sent to registered email for verifying and activating account")
        else:
            return data
        
    def get_jwt_token(self,data):
        user=auth.authenticate(username=data['username'],password=data['password'])
        if not user:
            return {'message': "Invalid Credentials"}
        refresh=RefreshToken.for_user(user)
        return  {
            'messsage':'Login Success!',
            'data':{
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                }
            }