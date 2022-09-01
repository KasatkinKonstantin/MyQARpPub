import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture()
def prepare_testing():
   """Подготовка к тестированию. Запускаем браузер Chrome на весь экран и авторизуемся на сайте PetFriends"""
   chrome_options = webdriver.ChromeOptions()
   chrome_options.add_argument('--start-maximized')
   driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
   driver.get('http://petfriends.skillfactory.ru/login')
   driver.find_element(By.ID, 'email').send_keys('kasatkin@kasatkin.ru')
   driver.find_element(By.ID, 'pass').send_keys('12345')
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   yield driver

   driver.quit()