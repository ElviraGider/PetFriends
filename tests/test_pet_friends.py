import requests
from api import PetFriends
from settings import *
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Check that the response to the request comes with the status 200 and in the body of the response there is a key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_list_of_pets_valid_key(filter=''):
    """Checking the possibility of getting a pets list. Status 200 and the pets list """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(result)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_pet_without_photo_valid(name=pet_without_photo['name'], animal_type=pet_without_photo['animal_type'],
                                      age=pet_without_photo['age']):
    """Check the possibility of adding a pet without a photo.
    Status 200 in the response body, there is an added pet with the specified name"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == pet_without_photo['name']

def test_post_pet_with_photo_valid(
        name=pet_without_photo['name'],
        animal_type=pet_without_photo['animal_type'],
        age=pet_without_photo['age'],
        pet_photo='images\cat.jpg'
):
    """Check the ability to add a pet with a photo, the status is 200 and the response body has the value pet_photo"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert len(result['pet_photo']) > 0

def test_put_new_info_valid(
        name=pet_new_info['name'],
        animal_type=pet_new_info['animal_type'],
        age=pet_new_info['age']):
    """Check the possibility of changing the information about the pet"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    status, result = pf.put_new_info(auth_key, name, animal_type, age, pet_id['pets'][0]['id'])
    assert status == 200
    assert result['name'] == pet_new_info['name']

def test_post_new_foto_for_pet_valid(pet_photo='images\dog.jpg'):
    """Check if it is possible to add or change the photo to the pet,
    the status is 200 and the response body has the value pet_photo"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    status, result = pf.post_new_foto_for_pet(auth_key, pet_id['pets'][0]['id'], pet_photo)
    assert status == 200
    assert len(result['pet_photo']) > 0

def test_delete_pet_pass():
    """Check if an existing pet can be deleted"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(pet_id['pets']) == 0:
        pf.status, result = pf.post_pet_without_photo(auth_key, 'Bill', 'Dog', '4')
        _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    status, result = pf.delete_pet(auth_key, pet_id['pets'][0]['id'])
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id['pets'][0]['id'] not in my_pets.values()
    assert len(result) == 0


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Check that the api key request does not return status 200"""
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'This user wasn&#x27;t found in database' in result

def test_get_list_of_pets_invalid_key(filter=''):
    """Check if it's possible to get a list of pets with invalid auth_key. Status 403 and message"""
    auth_key = {'key': ''}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result

def test_post_new_pet_with_incorrect_data(name='%$#@!', animal_type='54321', age='100'):
    """Check the possibility of adding a pet with incorrect data, status 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert 'Provided data is incorrect' in result

def test_delete_not_my_pet_pass():
    """Checking the possibility of removing someone else's pet"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(pet_id['pets']) != 0:
        for i in range(len(pet_id['pets'])):
            _, result = pf.delete_pet(auth_key, pet_id['pets'][i]['id'])

    _, pet_id = pf.get_list_of_pets(auth_key, '')
    status, result = pf.delete_pet(auth_key, pet_id['pets'][0]['id'])

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id['pets'][0]['id'] not in my_pets.values()