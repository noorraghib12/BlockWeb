from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response
from rest_framework import status,generics,permissions,viewsets

class RegisterAPI(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[permissions.AllowAny]
    def perform_create(self, serializer):
        if serializer.is_valid(): 
            serializer.save()
            send_uuid_email(serializer.validated_data['email'])
            return Response({'message':"User partially registered! Please visit registered email for account verification token!"})


class VerifyRegistrationAPI(viewsets.ModelViewSet):
    serializer_class=VerifyRegistration
    queryset=User.objects.all()


    def get_object(self,email):
        obj_=self.queryset.get(email=email)
        return obj_
            

    def update(self,request,*args,**kwargs):
        
        instance=self.get_object(email=request.data['email'])
        data=request.data.copy()
        serializer=self.serializer_class(instance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(generics.UpdateAPIView):
    queryset=User.objects.all()
    serializer_class=LoginSerializer
    
    def update(self,request,*args,**kwargs):
        instance=self.get_object()
        serializer=self.get_serializer(instance,data=request.data)
        if serializer.is_valid():
            return serializer.get_jwt_token(data=request.data)
        else:
            return Response({'message':'Invalid Credentials','data':serializer.errors})