from django.shortcuts import render
from .models import Treasure, Profile
from .serializers import TreasureSerializer, ProfileSerializer
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET','POST'])
def treasure_list(request):
   if request.method == 'GET': 
    treasures = Treasure.objects.all()
    serializer=TreasureSerializer(treasures, many=True)
    return JsonResponse({'treasures':serializer.data})
   if request.method == 'POST':
     serializer = TreasureSerializer(data = request.data)
     if serializer.is_valid():
       serializer.save()
       return Response(serializer.data, status=status.HTTP_201_CREATED)
     
@api_view(['GET','POST'])
def users_list(request):
   if request.method == 'GET': 
    users = Profile.objects.all()
    serializer=ProfileSerializer(users, many=True)
    return JsonResponse({'users':serializer.data})
   if request.method == 'POST':
     serializer = ProfileSerializer(data = request.data)
     if serializer.is_valid():
       serializer.save()
       return Response(serializer.data, status=status.HTTP_201_CREATED)     


"""
class TreasureViewSets(viewsets.ModelViewSet):
    queryset = Treasure.objects.all()
    serializer_class = TreasureSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
            
    
class ProfileViewSets(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
"""