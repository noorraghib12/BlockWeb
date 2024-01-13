from django.shortcuts import render
from serializers import *
from models import *
from serializers import *
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response
from rest_framework import status,generics,permissions,viewsets

class RegisterAPI(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[permissions.AllowAny]


class VerifyRegistrationAPI(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        data=self.request.data.copy()
        queryset=User.objects.get(email=data['user_email'])
        return queryset

    def update(self,serializer):
        serializer.save(is_active=True)