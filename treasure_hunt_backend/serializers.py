from rest_framework import serializers
from .models import Treasure, Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User
        fields = "__all__"
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
   # def update(self, instance, validated_data):
    #    if validated_data.get("password"):
     #       instance.set_password(validated_data['password'])
      #  instance.save()
       # return instance
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'treasures']
        
class TreasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treasure
        fields = ['id', 'name', 'latitude', 'longitude']