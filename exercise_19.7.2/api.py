import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> tuple[int, dict]:
        """Метод делает GET-запрос к API сервера и возвращает код ответа и ключ api в формате json,
        найденного по указанным email и password"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: dict, filter: str = '') -> tuple[int, dict]:
        """Метод делает GET-запрос к API сервера и возвращает код ответа и список питомцев в фотрмате json,
        найденных для указанных ключа api и фильтра"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: dict, name, animal_type, age, pet_photo: str) -> tuple[int, dict]:
        """Метод делает POST-запрос к API сервера и возвращает код ответа и данные
        добавленного питомца в формате json"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: dict, pet_id: str, name, animal_type, age) -> tuple[int, dict]:
        """Метод делает PUT-запрос к API сервера и возвращает код ответа и данные
        обновленного питомца в формате json"""
        data = {'name': name,
                'animal_type': animal_type,
                'age': age}
        headers = {'auth_key': auth_key['key']}
        res = requests.put(f'{self.base_url}api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: dict, pet_id: str) -> tuple[int, dict]:
        """Метод делает DELETE-запрос к API сервера и возвращает код ответа и список оставшихся питомцев
         в формате json"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(f'{self.base_url}api/pets/{pet_id}', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_simple(self, auth_key: dict, name, animal_type, age) -> tuple[int, dict]:
        """Метод делает POST-запрос к API сервера и возвращает код ответа и данные
        добавленного питомца в формате json"""
        data = {'name': name,
                'animal_type': animal_type,
                'age': age}
        headers = {'auth_key': auth_key['key']}
        res = requests.post(f'{self.base_url}api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_foto(self, auth_key: dict, pet_id: str, pet_photo: str) -> tuple[int, dict]:
        """Метод делает POST-запрос к API сервера и возвращает код ответа и данные
        добавленного питомца в формате json"""
        data = MultipartEncoder(fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(f'{self.base_url}api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

