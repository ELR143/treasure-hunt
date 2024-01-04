from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from django.contrib.auth.models import User
from ..models import Profile

class UserPostTests(APITransactionTestCase):
    reset_sequences = True
    def test_a_any_test(self):
        print("any_test")
        url = reverse("user-list")
        data = {"username": "electircboogaloo", "password": "ahh"}
        response = self.client.post(url, data) #id = 1
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username, "electircboogaloo")
        
    def test_b_create_user(self):
        print("test_create_user")
        url = reverse("user-list")
        data = {"username": "testeronee", "password": "stopLookingAtMyPassword"}
        response = self.client.post(url, data) #id = 2
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testeronee")
        
    def test_c_missing_input_data(self):
        print("missing_input_data")
        url = reverse("user-list")
        data = {"undername": "uhOh", "passwrd": "NOtGood"}
        response = self.client.post(url, data)#id = 3
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        
    def test_d_user_already_exists(self):
        print("test_user_already_exists")
        url = reverse("user-list")
        data = {"username": "twins", "password": "weAreTwinning"}
        data2 = {"username": "twins", "password": "howFun"}
        self.client.post(url, data) #id = 4
        response = self.client.post(url, data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_e_post_user_password_encrypted(self):
        print("post_user_password_encrypted")
        data = {"username": "findMe46", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 
        user = User.objects.get(username="findMe46")
        self.assertNotEqual(user.password, "iAmHidden")



class UserGetTests(APITransactionTestCase):
    reset_sequences = True
    def test_a_get_specific_user(self):
        print("test_get_specific_user")
        data = {"username": "findMe", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 
        url = reverse("user-detail", kwargs={"pk":1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, "findMe")

    def test_b_get_all_users(self):
        print("test_get_all_users")
        data = {"username": "findMe", "password": "iAmHidden"}
        data2 = {"username": "twins", "password": "howFun"}
        data3 = {"username": "twinning", "password": "veryfun"}
        self.client.post(reverse("user-list"), data) 
        self.client.post(reverse("user-list"), data2) 
        self.client.post(reverse("user-list"), data3) 
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 3)
        usernames = ["findMe", "twins", "twinning"]
        for username in usernames:
            self.assertTrue(User.objects.filter(username=username).exists())  

    def test_c_get_user_id_wrong(self):
        print("test_get_user_id_wrong")
        data = {"username": "findMe22", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data)  
        url = reverse("user-detail", kwargs={"pk":9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_d_get_user_id_invalid(self):
        print("get_user_id_invalid")
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 
        url = reverse("user-detail", kwargs={"pk":"notakey"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserPatchTests(APITransactionTestCase):
    reset_sequences = True
    def test_a_patch_user(self):
        print("test_a_patch_user")
        data = {"username": "findMe23", "password": "iAmHidden"}
        post_response = self.client.post(reverse("user-list"), data) 
        print(post_response.content)

        url = reverse("user-detail", kwargs={"pk":"1"})
        data2 = {"username": "findMe24", "first_name": "Liam", "last_name": "Yes", "email": "coolemail@gmail.com"}
        response = self.client.patch(url, data2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, "findMe24")
        self.assertEqual(User.objects.get().first_name, "Liam")
        self.assertEqual(User.objects.get().last_name, "Yes")
        self.assertEqual(User.objects.get().email, "coolemail@gmail.com")

    def test_b_patch_user_does_not_exist(self):
        print("patch_user_does_not_exist")
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 
        
        url = reverse("user-detail", kwargs={"pk":"9999"})
        data2 = {"username": "findMe25"}
        response = self.client.patch(url, data2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_c_patch_user_invalid_input(self):
        print("patch_user_invalid_input")
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 

        url = reverse("user-detail", kwargs={"pk":"iamnotanid"})
        data2 = {"username": "findMe25"}
        response = self.client.patch(url, data2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserDeleteTests(APITransactionTestCase):
    reset_sequences = True

    def test_a_delete_a_user(self):
        print("delete_a_user")
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 

        url = reverse("user-detail", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_b_delete_user_deletes_profile(self):
        print("delete_user_deletes_profile")
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 

        url = reverse("user-detail", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)

    def test_c_delete_user_does_not_exist(self):
        print("delete_user_does_not_exist")
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 

        url = reverse("user-detail", kwargs={"pk":"9999"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 1)

    def test_d_delete_user_invalid_id(self):
        print("delete_user_invalid_id")
        data = {"username": "findMe23", "password": "iAmHidden"}
        self.client.post(reverse("user-list"), data) 

        url = reverse("user-detail", kwargs={"pk":"notarealid"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 1)


# This test will work if/when encryption is added to prevent patching password returning an unencrypted password.
    # def test_e_patch_user_password_encrypted(self):
    #     print("post_user_password_encrypted")
    #     data = {"username": "findMe46", "password": "iAmHidden"}
    #     self.client.post(reverse("user-list"), data) 

    #     url = reverse("user-detail", kwargs={"pk":"1"})
    #     data2={"password": "AmIHidden"}
    #     response = self.client.patch(url, data2)

    #     user = User.objects.get(username="findMe46")
    #     self.assertNotEqual(user.password, "AmIHidden")


    


     