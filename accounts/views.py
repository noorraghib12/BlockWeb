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
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
    def create(self, request, *args, **kwargs):
        serialized=self.get_serializer(data=request.data)
        self.perform_create(serialized)
        send_uuid_email(serialized.validated_data['email'])
        return Response({'message':f"User partially registered! Please visit registered email {serialized.validated_data.get('email')} for account verification token!"},status=status.HTTP_206_PARTIAL_CONTENT)
    

class VerifyRegistrationAPI(viewsets.ModelViewSet):
    serializer_class=VerifyRegistration
    queryset=User.objects.all()
    lookup_field='email'
            

    def update(self,request,*args,**kwargs):
        instance=self.get_object()
        serializer=self.serializer_class(instance,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data,status=status.HTTP_202_ACCEPTED)
        
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
        
class ProfileViewset(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        if self.request.user:
            user=self.request.user
        else:
            username=self.request.data.get('username','')
            email=self.request.data.get('email','')
            user=User.objects.filter(Q(username=username) | Q(email=email))
            if not user.exists():
                raise User.DoesNotExist('Sorry the user does not exist~')
        return self.queryset.get(user=user)
        
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    
    def create(self,request,*args,**kwargs):
        serialized=self.get_serializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        self.perform_create(serialized)
        return Response(serialized.validated_data,status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        instance=self.get_object()
        serialized=self.get_serializer(instance)
        return Response(serialized.data,status=status.HTTP_200_OK)
    

    def update(self,request,*args,**kwargs):
        instance=self.get_object()
        serialized=self.get_serializer(instance,data=request.data,partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.validated_data,status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)