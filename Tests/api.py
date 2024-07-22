import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает СТАТУС запроса и результат
        в форме JSON с уникальным ключом пользователя AUTH_KEY, найденного по email и password"""

        headers = {
            'email': email,
            'password': passwd
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        """Метод делает запроск API сервера и возвращает СТАТУС запроса и результат
        в форме JSON (список питомцев согласно фильтру). Все питомцы - пустой фильтр,
        'my_pets' - собственные питомцы"""

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

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод ПОСТит на сервер данные о добавленном питомце и возвращает СТАТУС
        и результат в формате JSON с данными нового питомца"""

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
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по id и возвращает
        СТАТУС запроса и рез-т в формате JSON"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца (по id) и
        возвращает СТАТУС запроса и результат в формате JSON с обновленными данными"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
            }
        res = requests.put(self.base_url + 'api/pets/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод позволяет добавить фото питомцу (по id), возвращает СТАТУС запроса и ответ в формате JSON с указанием информации о фото"""

        data = MultipartEncoder(
        fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        )

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, data=data, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """Метод позволяет создавать нового питомца без фото, возвращает СТАТУС запроса и ответ в
        виде JSON с указанием информации о новом питомце"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result