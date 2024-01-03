from django.db import models
from django.contrib.auth.models import User

# Extending User Model Using a One-To-One Link
class Treasure(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    treasures = models.ManyToManyField('Treasure', related_name='owners', blank=True)

    def __str__(self):
        return self.user.username
    
