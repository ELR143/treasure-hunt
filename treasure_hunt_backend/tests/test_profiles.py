from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APITransactionTestCase
from django.contrib.auth.models import User
from ..models import Profile
#from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
#from .test_images import 

# Profiles Endpoint
## Get a list of all profiles 
## Get a single profile 
## Posts a new profile when a user is created 
## Patch a new avatar 
## Patch newly found treasure 
## Patching the collection keeps previous treasures
## Deletes a profile when the related user is deleted
## Erroneous tests too (: 
###TESTS ARE RUN ALPHABETICALLY AND MUST START WITH test

class GetProfiles(APITransactionTestCase):
    reset_sequences=True
    # These test creates user and test for a profile is created with the user
    def test_a_get_single_profile(self):
        urlu= reverse("user-list")
        data={"username": 'created-user-2',"password":'admin'}
        self.client.post(urlu,data)
        urlp=reverse('profile-detail',kwargs={'pk':1})
        response= self.client.get(urlp)   
        #print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,{"id": 1,"user": 1, "avatar":"http://testserver/default.jpg", "treasures":[]})

    def test_b_get_all_profiles(self):
        urlu= reverse("user-list")
        data={"username": 'created-user',"password":'admin'}
        data2 ={"username": 'created-user-2',"password":'admin'}
        self.client.post(urlu,data)
        self.client.post(urlu,data2)
        urlp= reverse("profile-list")
        response= self.client.get(urlp)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,[{"id": 1, "user": 1, "avatar": "http://testserver/default.jpg", "treasures": []},{"id": 2, "user": 2, "avatar": "http://testserver/default.jpg", "treasures": []}])

    def test_c_get_single_profile_not_found(self):
        url=reverse("profile-detail",kwargs={"pk":1}) 
        response =self.client.get(url) 
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
'''
class PatchProfiles(APITransactionTestCase):
    reset_sequences=True
    def test_a_patch_avatar_in_profile(self):
        
        newPhoto.image = SimpleUploadedFile(name='magikarp.png', content=open(".test_images", 'rb').read(), content_type='image/png')
        data = {"username": "findMe23", "password": "iAmHidden"}
        urlu= reverse("user-list")
        self.client.post(urlu,data)
        urlp= reverse("profile-detail",kwargs={"pk":1})
        data2={"avatar":newPhoto}
        response= self.client.patch(urlp,data2)
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,{"id": 1,"user": 1,"avatar": "magikarp.png","treasures": []})
 '''   
class DeleteProfile(APITransactionTestCase):
    reset_sequences=True
    def test_a_delete_a_profile_when_user_is_deleated(self):
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 
        urlu = reverse("user-detail", kwargs={"pk":"1"})
        self.client.delete(urlu)
        urlp=reverse("profile-detail",kwargs={"pk":1})
        response= self.client.get(urlp)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    
    