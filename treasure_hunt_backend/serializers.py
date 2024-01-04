from rest_framework import serializers
from .models import Treasure, Profile
from django.contrib.auth.models import User

class TreasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treasure
        fields = ['id', 'name', 'latitude', 'longitude']
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'treasures']
        
class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User
        fields = ["id", "username", "password"]
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user