import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

invalid_email = 'test@test.qa'
invalid_password = '12345 '

pet_without_photo = {'name': 'Jack', 'animal_type': 'cat', 'age': '2'}
pet_new_info= {'name': 'Bill', 'animal_type': 'Dog', 'age': '5'}