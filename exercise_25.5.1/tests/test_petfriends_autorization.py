import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest_check as check


def test_show_my_pets(prepare_testing):
   driver = prepare_testing
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   driver.implicitly_wait(5)
   images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
       check.not_equal(images[i].get_attribute('src'), '', f'{i+1}-ая карточка питомца. Тест на фото')
       check.not_equal(names[i].text, '', f'{i+1}-ая карточка питомца. Тест на имя')
       check.not_equal(descriptions[i].text, '', f'{i+1}-ая карточка питомца. Тест на описание')
       check.is_in(', ', descriptions[i].text, f'{i+1}-ая карточка питомца. Тест на описание')
       parts = descriptions[i].text.split(", ")
       check.greater(len(parts[0]), 0, f'{i+1}-ая карточка питомца. Тест на породу')
       check.greater(len(parts[1]), 0, f'{i+1}-ая карточка питомца. Тест на возраст')


def test_mypets(prepare_testing):
    driver = prepare_testing
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы"))).click()

    photo = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//th[@scope="row"]/img')))

    info = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td')))

    info1 = wait.until(EC.presence_of_all_elements_located(((By.XPATH, '//tbody/tr/td[@class="smart_cell"]'))))

    info = [x.text for x in info if x not in info1]

    kol = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]'))).text.split('Питомцев: ')[1]

    i = 0
    kol1 = ''
    while kol[i].isdigit():
        kol1 += kol[i]
        i += 1

    kol_photo = 0
    for i in photo:
        if i.get_attribute('src') != '':
            kol_photo +=1

    names = []
    for i in range(0, len(info), 3):
        names.append(info[i])

    list_of_pets = []
    for i in range(0, len(info), 3):
        list_of_pets.append([info[j] for j in range(i, i+3)])

    #Проверяем, что в списке присутсвуют все питомцы
    assert len(info)/3 == float(kol1)

    #Проверяем, что хотя бы у половины питомцев есть фото
    assert kol_photo >= float(kol1)/2

    #Проверяем, что у всех питомцев заполнены имя, порода и возраст
    for i in info:
        assert i != ''

    #Проверяем, что у всех питомцев разные имена
    assert len(names) == len(set(names))

    #Проверяем, что в списке нет одинаковых питомцев
    for i in range(len(list_of_pets)):
        for j in range(i+1, len(list_of_pets)):
            assert list_of_pets[i] != list_of_pets[j]