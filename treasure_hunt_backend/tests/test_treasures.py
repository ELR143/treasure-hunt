from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from django.contrib.auth.models import User
from ..models import Treasure
from ...profile_images import magikarp

# Treasures Endpoint
## Get a list of all available treasures 
## Get details of a specific treasure 
## Post a new treasure 
## Patch treasure details (admin only?) 
## Delete treasure (admin only?)
## Erroneous tests too (: 
###TESTS ARE RUN ALPHABETICALLY AND MUST START WITH test

urlAll = reverse("treasure-list")
urlError = reverse("treasure-detail", kwargs={"pk":2000})
url1 = reverse("treasure-detail", kwargs={"pk":1})
url2 = reverse("treasure-detail", kwargs={"pk":2})

gold = {"name": "Gold", "latitude": 500, "longitude": 500}
silver = {"name": "Silver", "latitude": 500, "longitude": 500}

class TreasureGetTests(APITransactionTestCase): 
    reset_sequences = True
    
    def test_returns_all_treasures(self):
        # print("test_returns_all_treasures")
        
        self.client.post(urlAll, gold) 
        self.client.post(urlAll, silver) 
        
        response = self.client.get(urlAll)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.count(), 2)
        
    
    def test_returns_a_single_treasure(self):
        # print("test_returns_a_single_treasure")
        
        self.client.post(urlAll, gold) 
        self.client.post(urlAll, silver) 
        
        response = self.client.get(url1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "name": "Gold", "latitude": 500, "longitude": 500})
        
    def test_error_when_treasure_to_get_cant_be_found(self):
        # print("test_error_when_treasure_cant_be_found")
        
        response = self.client.get(urlError)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_accounts_for_empty_treasure_list(self):
        # print("test_accounts_for_empty_treasure_list")
        
        response = self.client.get(urlAll)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.count(), 0)

class TreasurePostTests(APITransactionTestCase): 
    reset_sequences = True
    
    def test_creates_a_new_treasure(self):
        # print("test_creates_a_new_treasure")
        
        self.assertEqual(Treasure.objects.count(), 0)        
        
        response = self.client.post(urlAll, gold) 
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Treasure.objects.count(), 1)
        
    def test_can_make_treasure_with_same_name_in_different_location(self):
        # print("test_can_make_treasure_with_same_name_in_different_location")
        
        self.client.post(urlAll, gold) 
        
        response = self.client.post(urlAll, {"name": "Gold", "latitude": 1000, "longitude": 1000}) 
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Treasure.objects.filter(name__exact="Gold").count(), 2)
        self.assertEqual(Treasure.objects.filter(longitude__exact=500).count(), 1)
        
class TreasurePatchTests(APITransactionTestCase): 
    reset_sequences = True
    
    def test_change_longitude_of_treasure(self):
        # print("test_change_longitude_of_treasure")
        
        self.client.post(urlAll, gold) 
        self.client.post(urlAll, silver) 
        
        newData = {"longitude": 300}
        response = self.client.patch(url2, newData)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.get(name__exact="Silver").longitude, 300)
    
    def test_change_latitude_of_treasure(self):
        # print("test_change_latitude_of_treasure")
        
        self.client.post(urlAll, gold) 
        self.client.post(urlAll, silver) 
        
        newData = {"latitude": 300}
        response = self.client.patch(url2, newData)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.get(name__exact="Silver").latitude, 300)
        
    def test_change_name_of_treasure(self):
        # print("test_change_name_of_treasure")
        
        self.client.post(urlAll, gold) 
        
        newData = {"name": "Bronze"}
        response = self.client.patch(url1, newData)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.get(id__exact=1).name, "Bronze")
    
class TreasureDeleteTests(APITransactionTestCase): 
    reset_sequences = True
    
    def test_remove_a_specified_treasure(self):
        # print("test_remove_a_treasure")
        
        self.client.post(urlAll, gold)         
        self.client.post(urlAll, silver)         
        response = self.client.delete(url2)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Treasure.objects.count(), 1)
        self.assertEqual(Treasure.objects.get(name__exact="Gold").name, "Gold")

    def test__error_when_treasure_to_delete_cant_be_found(self):
        # print("test_error_when_treasure_cant_be_found")
        
        response = self.client.delete(urlError)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)