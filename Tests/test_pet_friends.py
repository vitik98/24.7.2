from api import PetFriends
from settings import valid_email, valid_password, wrong_email, wrong_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем на статус 200 и получение ключа key в ответе"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=""):
    """Проверяем, что общий список не пустой"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)  #запрашиваем ключ и записываем его в переменную
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pets_valid_data(name="Мурзик", animal_type='кот', age='1', pet_photo='images/cat1.jpg'):
    """Проверяем возможность создать нового питомца с правильными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) #получаем полный путь к фото и записываем в переменную

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_get_my_pets_with_valid_key(filter="my_pets"):
    """Проверяем, что список созданных нами питомцев не пустой"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_create_pet_simple_valid_data(name="Мурзик", animal_type='кот', age=1):
    """Проверяем возможность создать нового питомца с правильными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления своего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Тузик", "пес", 5, "images/dog1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_pet_info(name="Котяра", animal_type="кот", age=1):
    """Проверяем возможность обновления инфо о питомце по id"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('У меня еще нет питомцев')


def test_successful_add_photo(pet_photo='images/cat2.jpg'):
    """Проверяем возможность добавить фото в карточку питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Чижик', 'кот', 3)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_photo(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert 'photo' in result or 'pet_photo' in result


def test_negative_add_wrong_photo(pet_photo='images/htsm.pdf'):
    """Проверяем возможность добавления другого файла вместо фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Пупс', 'кот', 3)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo(auth_key, pet_id, pet_photo)

    assert status == 500


def test_negative_get_api_key_for_wrong_email(email=wrong_email, password=valid_password):
    """Проверяем возможность получения ключа с неправильным email"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_negative_get_api_key_for_wrong_password(email=valid_email, password=wrong_password):
    """Проверяем возможность получения ключа с неправильным паролем"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_negative_create_pet_simple_wrong_age(name='Милаха', animal_type='черепаха', age=-150):
    """Проверяем возможность создания питомца с отрицательным возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
# БАГ Смотрим техзадание, почему поле "age" принимает отрицательные значения!


def test_negative_create_pet_simple_str_age(name='Georg', animal_type='corgi', age='twelve'):
    """Проверяем невозможность создания питомца с возрастом в формате str"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
# БАГ В сваггере указан допустимый формат ячейки "age" как int!


def test_negative_create_incorrect_pet_simple(name=None, animal_type=None, age =None):
    """Проверяем возможность создания питомца без заполнения обязательных полей name, animal_type и age"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400


def test_negative_update_pet_info_none(name=' ', animal_type='fox', age=5):
    """Проверяем возможность обновить обязательное значениe name в карточке своего питомца на пустое"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Муська", "котяра", 7)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status == 400
# БАГ Поле "name" является обязательным при создании карточки питомца, менять на пустое значение недопустимо.


def test_negative_update_pet_info_too_large(name='Meow'*256, animal_type='cat', age=1):
    """Проверяем возможность обновить данные своего питомца на очень большое значение"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Муська", "котяра", 7)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status == 400
# БАГ Нет ограничений на количество символов в имени.


def test_negative_create_pet_simple_too_large_name(name='G'*300, animal_type='corgi', age=12):
    """Проверяем возможность создания питомца с очень большим именем"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
# БАГ Нет ограничений на количество символов в имени.