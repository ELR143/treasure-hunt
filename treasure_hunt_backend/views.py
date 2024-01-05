from django.shortcuts import render
from .models import Treasure, Profile
from django.contrib.auth.models import User
from .serializers import TreasureSerializer, ProfileSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from rest_framework. decorators import api_view


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def list(self, request, *args, **kwargs):  
        response = super(UserViewSets, self).list(request, *args, **kwargs)  
        response.data = {"users": response.data}
        return response  

class ProfileViewSets(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def list(self, request, *args, **kwargs):  
        response = super(ProfileViewSets, self).list(request, *args, **kwargs)  
        response.data = {"profiles": response.data}
        return response  

class TreasureViewSets(viewsets.ModelViewSet):
    queryset = Treasure.objects.all()
    serializer_class = TreasureSerializer
    
    def list(self, request, *args, **kwargs):  
        response = super(TreasureViewSets, self).list(request, *args, **kwargs)  
        response.data = {"treasure": response.data}
        return response  