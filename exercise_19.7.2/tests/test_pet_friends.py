from api import PetFriends
from settings import valid_email, valid_password, not_valid_password, not_valid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем возможность получения ключа api с корректными учетными данными"""

    # Получаем ключ api
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_data(filter='my_pets'):
    """Проверяем возможность получения списка питомцев с корректными фильтром и ключем api"""

    # Получаем ключ api и и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Получаем список своих питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбос', animal_type='двортерьер', age='4', pet_photo='images/dog.jpg'):
    """Проверяем возможность добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_delete_self_pet_with_valid_data():
    """Проверяем возможность удаления питомца с корректными данными"""

    # Получаем ключ api в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Получаем список своих питомцев
    my_pets = pf.get_list_of_pets(auth_key, 'my_pets')[1]

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
        my_pets = pf.get_list_of_pets(auth_key, 'my_pets')[1]

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status = pf.delete_pet(auth_key, pet_id)[0]

    # Ещё раз запрашиваем список своих питомцев
    my_pets = pf.get_list_of_pets(auth_key, 'my_pets')[1]

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_self_pet_info_with_valid_data(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце с корректными данными"""

    # Получаем ключ api и список своих питомцев
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    my_pets = pf.get_list_of_pets(auth_key, "my_pets")[1]

    # Если список не пустой, то пробуем обновить имя, породу и возраст первого питомца в списке
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#Test №1
def test_add_new_pet_simple_with_valid_data(name='Шарик', animal_type='собакен', age=6):
    """Проверяем, возможность добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


#Test №2
def test_add_photo_with_valid_data(pet_photo='images/pop.jpg'):
    """Проверяем возможность обновить фото питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Получаем список своих питомцев
    my_pets = pf.get_list_of_pets(auth_key, 'my_pets')[1]

    # Если список не пустой, то пробуем обновить фото первого питомца в списке
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_foto(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и поле pet_photo не пустое
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#Test №3
def test_get_api_key_for_not_valid_user(email=not_valid_email, password=not_valid_password):
    """Проверяем невозможность получения ключа api с некорректными учетными данными"""

    # Получаем ключ api
    status = pf.get_api_key(email, password)[0]

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


#Test №4
def test_add_photo_with_not_valid_id(pet_photo='images/cat.jpg'):
    """Проверяем невозможность обновления фото несуществующего питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Пытаемся обновить фото питомца которого нет в базе
    status = pf.add_pet_foto(auth_key, 'no_valid_id', pet_photo)[0]

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500


#Test №5
def test_add_photo_with_bad_file(pet_photo='images/bad_image.jpg'):
    """Проверяем невозможность обновить фото питомца битым файлом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    # Получаем список своих питомцев
    my_pets = pf.get_list_of_pets(auth_key, 'my_pets')[1]

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status = pf.add_pet_foto(auth_key, my_pets['pets'][0]['id'], pet_photo)[0]
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 500
    else:
        # Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#Test №6
def test_delete_pet_with_empty_id():
    """Проверяем невозможность удаления питомца c id равному пустой строке"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Пытаемся удалить питомца с id равному пустой строке
    status = pf.delete_pet(auth_key, '')[0]

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 404


#Test №7
def test_delete_pet_with_not_valid_id():
    """Проверяем невозможность удаления питомца с некорректным id"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Пытаемся удалить питомца с некорректным id
    status = pf.delete_pet(auth_key, 'not_valid_id')[0]

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 404


#Test №8
def test_update_pet_info_with_not_valid_id(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем невозможность обновления информации о питомце с некорректным id"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Пытаемся обновить информацию о питомце с некорректным id
    status, result = pf.update_pet_info(auth_key, 'not_valid_id', name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


#Test №9
def test_get_all_pets_with_no_valid_key(filter='my_pets'):
    """Проверяем невозможность получить список питомцев с некорректным ключем api"""

    # Пытаемся получить список питомцев с некорректным ключем api
    status, result = pf.get_list_of_pets({'key': ''}, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


#Test №10
def test_get_all_pets_with_no_valid_filter(filter='no_filter'):
    """Проверяем невозможность получить список питомцев с некорректным фильтром"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Пытаемся получить список питомцев с некорректным фильтром
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500


#Test №11
def test_add_new_pet_simple_with_no_valid_data(name='', animal_type='', age=''):
    """Проверяем невозможность добавления питомца без фото с некорректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Пытаемся добавить питомца с некорректными данными (пустые поля)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500


#Test №12
def test_add_new_pet_with_no_valid_data(name='', animal_type='', age='', pet_photo='images/bad_image.jpg'):
    """Проверяем невозможность добавления питомца с некорректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Пытаемся добавить питомца с некорректными данными (пустые поля и битый файл)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500







