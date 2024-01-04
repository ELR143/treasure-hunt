from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from django.contrib.auth.models import User
from ..models import Treasure

# Treasures Endpoint
## Get a list of all available treasures 
## Get details of a specific treasure 
## Post a new treasure 
## Patch treasure details (admin only?) 
## Delete treasure (admin only?)
## Erroneous tests too (: 
###TESTS ARE RUN ALPHABETICALLY AND MUST START WITH test

class TreasureDeleteTests(APITestCase): 
    def test_a_remove_a_treasure(self):
        # print("test_a_remove_a_treasure")
        
        url = reverse("treasure-list")
        self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id =1
        self.client.post(url, {"name": "forFake", "latitude": 500, "longitude": 500}) # id =2
        
        response = self.client.delete(reverse("treasure-detail", kwargs={"pk":2}))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Treasure.objects.count(), 1)
        self.assertEqual(Treasure.objects.get(name__exact="forReal").name, "forReal")

    def test_b_error_when_treasure_to_delete_cant_be_found(self):
        # print("test_b_error_when_treasure_cant_be_found")
        
        response = self.client.delete(reverse("treasure-detail", kwargs={"pk":2000}))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TreasureGetTests(APITestCase): 
    def test_a_returns_all_treasures(self):
        # print("test_c_returns_all_treasures")
        
        url = reverse("treasure-list")
        self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id = 3
        self.client.post(url, {"name": "forFake", "latitude": 500, "longitude": 500}) # id = 4
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.count(), 2)
        
    
    def test_b_returns_a_single_treasure(self):
        # print("test_d_returns_a_single_treasure")
        
        url = reverse("treasure-list")
        self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id = 5
        self.client.post(url, {"name": "forFake", "latitude": 500, "longitude": 500}) # id = 6
        
        response = self.client.get(reverse("treasure-detail", kwargs={"pk":5}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 5, "name": "forReal", "latitude": 500, "longitude": 500})
        
    def test_c_error_when_treasure_to_get_cant_be_found(self):
        # print("test_e_error_when_treasure_cant_be_found")
        
        response = self.client.get(reverse("treasure-detail", kwargs={"pk":2000}))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_d_accounts_for_empty_trasure_list(self):
        # print("test_f_accounts_for_empty_trasure_list")
        
        response = self.client.get(reverse("treasure-list"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.count(), 0)

    
class TreasurePatchTests(APITestCase): 
    def test_a_change_longitude_of_treasure(self):
        # print("test_g_change_longitude_of_treasure")
        
        url = reverse("treasure-list")
        self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id = 7
        self.client.post(url, {"name": "forFake", "latitude": 500, "longitude": 500}) # id = 8
        
        newData = {"longitude": 300}
        response = self.client.patch(reverse("treasure-detail", kwargs={"pk":8}), newData)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.get(name__exact="forFake").longitude, 300)
    
    def test_b_change_latitude_of_treasure(self):
        # print("test_h_change_latitude_of_treasure")
        
        url = reverse("treasure-list")
        self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id = 9
        self.client.post(url, {"name": "forFake", "latitude": 500, "longitude": 500}) # id = 10
        
        newData = {"latitude": 300}
        response = self.client.patch(reverse("treasure-detail", kwargs={"pk":10}), newData)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.get(name__exact="forFake").latitude, 300)
        
    def test_c_change_name_of_treasure(self):
        # print("test_i_change_name_of_treasure")
        
        url = reverse("treasure-list")
        self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id = 11
        self.client.post(url, {"name": "forFake", "latitude": 500, "longitude": 500}) # id = 12
        
        newData = {"name": "forMaybe"}
        response = self.client.patch(reverse("treasure-detail", kwargs={"pk":12}), newData)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Treasure.objects.get(id__exact=12).name, "forMaybe")
    
class TreasurePostTests(APITestCase): 
    def test_a_creates_a_new_treasure(self):
        # print("test_j_creates_a_new_treasure")
        
        url = reverse("treasure-list")
        self.assertEqual(Treasure.objects.count(), 0)        
        
        response = self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id = 13
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Treasure.objects.count(), 1)
        
    def test_b_can_make_treasure_with_same_name_in_different_location(self):
        # print("test_k_can_make_treasure_with_same_name_in_different_location")
        
        url = reverse("treasure-list")
        self.client.post(url, {"name": "forReal", "latitude": 500, "longitude": 500}) # id = 14
        
        response = self.client.post(url, {"name": "forReal", "latitude": 1000, "longitude": 1000}) # id = 15
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Treasure.objects.filter(name__exact="forReal").count(), 2)
        self.assertEqual(Treasure.objects.filter(longitude__exact=500).count(), 1)