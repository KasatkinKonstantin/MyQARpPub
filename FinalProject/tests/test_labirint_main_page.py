import pytest
from pages.MainPage import MainPage
import time


def test_check_main_search(web_browser):
    """ Проверка, что основной поиск работает нормально. """

    page = MainPage(web_browser)

    page.search = 'осень'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() == 60

    # Проверяем, что пользователь нашел соответствующие книги:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'осен' in title.lower(), msg


def test_check_main_exact_search(web_browser):
    """ Проверка, что точный поиск работает нормально. """

    page = MainPage(web_browser)

    page.search = 'осень в сокольниках'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь нашел соответствующие книги:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'осень в сокольниках' in title.lower(), msg


def test_check_wrong_input_in_search(web_browser):
    """ Проверка, что ввод с неправильной раскладки клавиатуры работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести «осень» с английской клавиатуры:
    page.search = 'jctym'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь нашел соответствующие книги:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'осен' in title.lower(), msg


def test_check_wrong_input(web_browser):
    """ Проверка, что поиск при вводе с орфографическими ошибками работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести «карамель» с тремя ошибками:
    page.search = 'коромиль'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь видит страницу с результатами поиска:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert title == 'Все, что мы нашли в Лабиринте по запросу «карамель»', msg


def test_check_input_numbers_in_search(web_browser):
    """ Проверка, что при вводе цифр поиск работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести несколько цифр:
    page.search = '12399'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь нашел соответствующие товары:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert '12399' in title, msg


def test_check_input_symbols_in_search(web_browser):
    """ Проверка, что при вводе знаков поиск работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести несколько знаков:
    page.search = '%!*'
    page.search_run_button.click()

    # Проверяем, что в списоке нет найденных товаров:
    assert page.products_titles.count() == 0

    # Проверяем, что появилось сообщение, что ничего не найдено:
    assert page.msg_search_er.get_text() == "Мы ничего не нашли по вашему запросу! Что делать?"


def test_check_search_electronic_books(web_browser):
    """ Проверка, что поиск электронных книг работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Убираем из результатов поиска другие товары, нажимаем на кнопку "Прочие товары":
    page.without_others_products_button.click()

    # Убираем из результатов поиска бумажные книги, нажимаем на кнопку "Бумажные книги":
    page.without_paper_books_button.click()
    time.sleep(10)

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() >= 1

    # Проверяем, что найдены электронные книги:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' in title.lower(), msg


def test_check_search_paper_books(web_browser):
    """ Проверка, что поиск бумажных книг работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Убираем из результатов поиска электронные книги, нажимаем на кнопку "Электронные книги":
    page.without_electronic_books_button.click()

    # Убираем из результатов поиска прочие товары, нажимаем на кнопку "Прочие товары":
    page.without_others_products_button.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' not in title.lower(), msg


def test_check_search_expected(web_browser):
    """ Проверка, что фильтр товаров со статусом "Ожидается" работает нормально. """

    page = MainPage(web_browser)

    page.search = 'золото'
    page.search_run_button.click()

    # Убираем из результатов поиска товары по предзаказу, нажимаем на кнопку "Предзаказ":
    page.sort_products_by_type_order.click()

    # Убираем из результатов поиска товары в наличии, нажимаем на кнопку "В наличии":
    page.sort_products_by_type_in_stock_is.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_waiting.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'ожидается' in title.lower(), msg


def test_check_search_in_stock(web_browser):
    """ Проверка, что фильтр товаров "В наличии" работает нормально. """

    page = MainPage(web_browser)

    page.search = 'краска'
    page.search_run_button.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Нет в продаже":
    page.sort_products_by_type_out_of_stock.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Ожидаются":
    page.sort_products_by_type_waiting.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Предзаказ":
    page.sort_products_by_type_order.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() == 60

    # Проверяем, что найдены товары, которые имеются в наличии, их можно положить в корзину:
    for title in page.products_in_stock.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'корзину' in title.lower(), msg


def test_check_search_electronic_books_another_way(web_browser):
    """ Проверка, что фильтр электронных книг в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Бумажные книги":
    page.paper_books.click()

    # Отжимаем галочку в строке "Другие товары":
    page.other_goods.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    time.sleep(10)

    # Проверяем, что найдены электронные книги:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' in title.lower(), msg


def test_check_search_paper_books_another_way(web_browser):
    """ Проверка, что фильтр бумажных книг в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Электронные книги":
    page.electronic_books.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Другие товары":
    page.other_goods.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' not in title.lower(), msg

def test_check_search_other_goods(web_browser):
    """ Проверка, что фильтр других товаров в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'ластик'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Бумажные книги":
    page.paper_books.click()

    page.show_button.scroll_to_element()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() == 60


def test_check_search_what_to_read(web_browser):
    """ Проверка, что кнопка "Что почитать: выбор редакции" работает. """

    page = MainPage(web_browser)

    page.what_to_read_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles_large.count() >= 1


def test_check_button_what_to_read(web_browser):
    """ Проверка, что кнопка "Что почитать: выбор редакции" ведет на нужную страницу. """

    page = MainPage(web_browser)

    page.what_to_read_button.click()

    # Проверяем, что пользователь видит страницу с рекомендациями книг от редакции:
    assert page.page_title.get_text() == "Что почитать: выбор редакции"


def test_check_button_fair(web_browser):
    """ Проверка, что кнопка "Премьеры книжной ярмарки" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Премьеры книжной ярмарки":
    page.fair_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.fair_content.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'ярмарк' in title.lower(), msg


def test_check_search_best_buy(web_browser):
    """ Проверка, что кнопка "Лучшая покупка дня" работает. """

    page = MainPage(web_browser)

    page.best_buy_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_pubhouse.count() >= 1


def test_check_button_best_buy(web_browser):
    """ Проверка, что кнопка "Лучшая покупка дня" ведет на нужную страницу. """

    page = MainPage(web_browser)

    page.best_buy_button.click()

    # Проверяем, что пользователь видит страницу с рекомендациями книг от редакции:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'главные книги' in title.lower(), msg


def test_check_search_discounts_books(web_browser):
    """ Проверка, что кнопка "Больше книг со скидками" работает. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Больше книг со скидками":
    page.discounts_button.click()

    # Проверяем, что пользователь видит книги со скидками:
    for title in page.discounts_books.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert '%' in title, msg


def test_check_button_discounts_books(web_browser):
    """ Проверка, что кнопка "Больше книг со скидками" ведет на нужную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Больше книг со скидками":
    page.discounts_button.click()

    # Проверяем, что пользователь видит страницу с заголовком "Главные книги":
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'главные книги' in title.lower(), msg


def test_check_search_today(web_browser):
    """ Проверка, что кнопка "Читатели выбирают сегодня" работает. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Читатели выбирают сегодня":
    page.today_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_books.count() >= 1


def test_check_button_today(web_browser):
    """ Проверка, что кнопка "Читатели выбирают сегодня" ведет на нужную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Читатели выбирают сегодня":
    page.today_button.click()

    # Проверяем, что пользователь видит страницу с заголовком "Главные книги":
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'главные книги' in title.lower(), msg


def test_check_search_books(web_browser):
    """ Проверка, что фильтр поиска только книг работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зверь'
    page.search_run_button.click()

    # Убираем из результатов поиска другие товары, нажимаем на кнопку "Прочие товары":
    page.without_others_products_button.click()

    # Проверяем, что нпользователь может видеть список книг:
    assert page.products_books.count() == 60


def test_check_button_now(web_browser):
    """ Проверка, что кнопка "Лабиринт. Сейчас" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Лабиринт. Сейчас":
    page.now_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.active_menu_item.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'лабиринт. сейчас' in title.lower(), msg


def test_check_button_kids(web_browser):
    """ Проверка, что кнопка "Детский навигатор — что читать детям и с детьми" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Детский навигатор — что читать детям и с детьми":
    page.kids_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.active_menu_item.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'детский навигатор' in title.lower(), msg


def test_check_button_teenagers(web_browser):
    """ Проверка, что кнопка "Книги для подростков" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Книги для подростков":
    page.teenagers_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.heading_on_the_page.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'подростков' in title.lower(), msg


def test_check_button_leaders(web_browser):
    """ Проверка, что кнопка "Книжные лидеры продаж" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Книжные лидеры продаж":
    page.leaders_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'рейтинг продаж' in title.lower(), msg


def test_check_button_delivery(web_browser):
    """ Проверка, что кнопка "Доставка и оплата" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Доставка и оплата":
    page.delivery_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.section_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'доставка' in title.lower(), msg


def test_check_button_certificates(web_browser):
    """ Проверка, что кнопка "Сертификаты" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Сертификаты":
    page.certificates_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.section_content.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'сертификаты' in title.lower(), msg


def test_check_button_ratings(web_browser):
    """ Проверка, что кнопка "Рейтинги" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Рейтинги":
    page.ratings_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'рейтинг' in title.lower(), msg


def test_check_button_novelties(web_browser):
    """ Проверка, что кнопка "Новинки" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Новинки":
    page.novelties_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'новые книги' in title.lower(), msg


def test_check_button_discounts(web_browser):
    """ Проверка, что кнопка "Скидки" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Скидки":
    page.discounts_books_button.click()

    # Проверяем, что пользователь видит книги со скидками:
    for title in page.discounts_books.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert '%' in title, msg


def test_check_button_contacts(web_browser):
    """ Проверка, что кнопка "Контакты" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Контакты":
    page.contacts_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'контакты' in title.lower(), msg


def test_check_button_support(web_browser):
    """ Проверка, что кнопка "Поддержка" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Поддержка":
    page.support_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.section_title_support.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'публичные вопросы' in title.lower(), msg


def test_check_button_export(web_browser):
    """ Проверка, что кнопка "141 пункт самовывоза" горизонтального меню ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "141 пункт самовывоза":
    page.export_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.section_title_export.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'доставка' in title.lower(), msg


def test_check_button_novelties_books(web_browser):
    """ Проверка, что кнопка "Книги: новинки 2022" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Книги: новинки 2022":
    page.novelties_books_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'новые книги' in title.lower(), msg


def test_check_button_reviews(web_browser):
    """ Проверка, что кнопка "Книжные обзоры и рецензии" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Книжные обзоры и рецензии":
    page.reviews_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.heading_reviews.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'обзоры и рецензии' in title.lower(), msg


def test_check_button_regulations(web_browser):
    """ Проверка, что кнопка "Правила" в разделе "Вам подарок!" ведет на правильную страницу. """

    page = MainPage(web_browser)

    # Нажимаем на кнопку "Правила":
    page.regulations_button.click()

    # Проверяем, что пользователь видит нужную страницу:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'купон' in title.lower(), msg


def test_check_search_authors(web_browser):
    """ Проверка, что фильтр списка авторов по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() == 60

    # Нажимаем на кнопку "Авторы" в горизонтальном меню:
    page.authors_button.click()

    # Проверяем, что пользователь видит список авторов, отобранных по заданному параметру поиска:
    for title in page.authors_names.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'зима' in title.lower(), msg


def test_check_search_author(web_browser):
    """ Проверка, что поиск страницы с книгами определенного автора работает правильно. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Нажимаем на кнопку "Авторы" в горизонтальном меню:
    page.authors_button.click()

    # Нажимаем на ФИО автора "Зима Владимир":
    page.our_author_button.click()

    # Проверяем, что пользователь видит страницу, посвященную искомому автору:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'зима владимир' in title.lower(), msg


def test_check_search_author_petrov(web_browser):
    """ Проверка, что поиск книг определенного автора работает правильно. """

    page = MainPage(web_browser)

    page.search = 'петров'
    page.search_run_button.click()

    # Нажимаем на кнопку "Авторы" в горизонтальном меню:
    page.authors_button.click()

    # Нажимаем на ФИО автора "Петров Петр":
    page.petrov_author_button.click()

    # Проверяем, что пользователь видит страницу, посвященную искомому автору:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'петров петр' in title.lower(), msg

    # Проверяем, что пользователь видит 24 книги:
    assert page.products_titles.count() == 24


def test_check_search_publishing_offices(web_browser):
    """ Проверка, что фильтр списка книжных издательств по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'золото'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() == 60

    # Нажимаем на кнопку "Изд-ва" в горизонтальном меню:
    page.publishing_offices_button.click()

    # Проверяем, что пользователь видит список издательств, отобранных по заданному параметру поиска:
    for title in page.publishing_offices.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'золот' in title.lower(), msg


def test_check_search_publishing_office(web_browser):
    """ Проверка, что поиск страницы с книгами определенного издательства работает правильно. """

    page = MainPage(web_browser)

    page.search = 'золото'
    page.search_run_button.click()

    # Нажимаем на кнопку "Изд-ва" в горизонтальном меню:
    page.publishing_offices_button.click()

    # Нажимаем на название издательства "Золотой лев":
    page.publishing_office_button.click()

    # Проверяем, что пользователь видит страницу, посвященную искомому издательству:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert title == 'Издательство «Золотой лев»', msg


def test_check_search_author_golden_lion(web_browser):
    """ Проверка, что поиск книг определенного издательства работает правильно. """

    page = MainPage(web_browser)

    page.search = 'золото'
    page.search_run_button.click()

    # Нажимаем на кнопку "Изд-ва" в горизонтальном меню:
    page.publishing_offices_button.click()

    # Нажимаем на название издательства "Золотой лев":
    page.publishing_office_button.click()

    # Нажимаем кнопку "Все книги":
    page.all_books_button.click()

    # Проверяем, что пользователь видит список книг:
    assert page.products_titles.count() >= 1


def test_check_search_product_series(web_browser):
    """ Проверка, что фильтр списка серий товаров по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'дворец'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() == 60

    # Нажимаем на кнопку "Серии" в горизонтальном меню:
    page.product_series_button.click()

    # Проверяем, что пользователь видит список серий товаров, отобранных по заданному параметру поиска:
    for title in page.product_series.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'дворец' in title.lower() or 'дворц' in title.lower(), msg


def test_check_search_product_part(web_browser):
    """ Проверка, что поиск страницы с товарами определенной серии работает правильно. """

    page = MainPage(web_browser)

    page.search = 'дворец'
    page.search_run_button.click()

    # Нажимаем на кнопку "Серии" в горизонтальном меню:
    page.product_series_button.click()

    # Нажимаем на название серии "Хрустальный дворец":
    page.product_part_button.click()

    # Проверяем, что пользователь видит страницу c товарами искомой серии:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'хрустальный дворец' in title.lower(), msg


def test_check_search_series_crystal_palace(web_browser):
    """ Проверка, что поиск товаров определенной серии работает правильно. """

    page = MainPage(web_browser)

    page.search = 'дворец'
    page.search_run_button.click()

    # Нажимаем на кнопку "Серии" в горизонтальном меню:
    page.product_series_button.click()

    # Нажимаем на название серии "Хрустальный дворец":
    page.product_part_button.click()

    # Проверяем, что пользователь видит список книг:
    assert page.products_titles.count() >= 1


def test_check_search_video(web_browser):
    """ Проверка, что фильтр списка видео по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'здоров'
    page.search_run_button.click()

    # Нажимаем на кнопку "Видео" в горизонтальном меню:
    page.video_button.click()

    # Проверяем, что пользователь может видеть список 25 видео, отобранных по заданному параметру поиска:
    assert page.video_products.count() == 25

    # проверяем, что в списке только названия видео со ссылками:
    for title in page.video_products.get_attribute('href'):
        msg = 'Wrong product in search "{}"'.format(title)
        assert title != '', msg


def test_check_search_themes(web_browser):
    """ Проверка, что фильтр Темы по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'кухня'
    page.search_run_button.click()

    # Нажимаем на кнопку "Темы" в горизонтальном меню:
    page.themes_button.click()

    # Проверяем, что пользователь может видеть список 6 тем, отобранных по заданному параметру поиска:
    assert page.themes_products.count() == 6

    # проверяем, что в списке названия тем со ссылками:
    for title in page.themes_products.get_attribute('href'):
        msg = 'Wrong product in search "{}"'.format(title)
        assert title != '', msg


def test_check_search_theme(web_browser):
    """ Проверка, что выбор определенной Темы по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'кухня'
    page.search_run_button.click()

    # Нажимаем на кнопку "Темы" в горизонтальном меню:
    page.themes_button.click()

    # Нажимаем на название темы "Литературная кухня. Вкусные рецепты для любимых читателей":
    page.theme_button.click()

    # проверяем, что пользователь видит нужную страницу:
    # Тест не проходит, т.к. страница не найдена
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'литературная кухня' in title.lower(), msg