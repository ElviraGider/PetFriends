import requests
import json
from requests_toolbelt import MultipartEncoder

class PetFriends:
    """API library to web application PetFriends"""
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """The method makes a request to the server API and returns the request status and the result in JSON format
        with the unique key of the user, found by the specified email and password"""
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """The method makes a request to the server API and returns the request status and the result in JSON format
        with the list of pets"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """The method makes a request to the API server to add a pet without a photo and
        returns the status of the request and the result in JSON format with information about the added pet"""
        data = MultipartEncoder(fields={'name': name, 'animal_type': animal_type, 'age': age})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_pet_with_photo(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """The method makes a request to the server API to add a pet with a photo and returns the status of the request
        and the result in JSON format with information about the added pet"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def put_new_info(self, auth_key: json, name: str, animal_type: str, age: str, pet_id: str) -> json:
        """The method makes a request to the server API to change the name of the pet by the specified ID and returns
        the status of the request and the result in JSON format with information about the changed pet,
        the photo is not changed"""
        data = MultipartEncoder(
            fields={'name': name, 'animal_type': animal_type, 'age': age})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """The method makes a request to the API server to delete the pet by the specified ID and
        returns the status of the request and the result in JSON format"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_new_foto_for_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """The method makes a request to the API server to add a photo to the pet card without a photo"""
        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result