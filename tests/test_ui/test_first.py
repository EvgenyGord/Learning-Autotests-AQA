import time

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.mark.parametrize("email, name, password", [
    ("test2@mail.ru", "User25", "qwertyu1"),
    ("test25@mail.ru", "User2566", "qwertyu1")
])
def test_function(email, name, password):
    print(f"Email: {email}, Name: {name}, Password: {password}")

@allure.epic("Аутентификация и авторизация")
@allure.feature("Регистрация пользователей")
@allure.suite("Смоук тесты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "ui")
@allure.label("owner", "QA - evgeny_gord")
@allure.id("TEST-123")
@allure.title("Проверка создания пользователя")
@allure.description("""
Этот тест проверяет:
- Регистрацию пользователя с позитивным сценарием
- Проверка успеха прохождения регистрации 
ИЛИ
- Проверка предупреждения, что пользователь уже создан с таким email
""")
@allure.link("https://jira.example.com/TEST-123", name="JIRA Task")
@allure.issue("BUG-456", "https://bugtracker.com/BUG-456")
@allure.testcase("TC-789", "https://testcase.com/TC-789")
def test_positive_registration(browser, base_url, wait, registration_data):
    # driver = webdriver.Chrome(service=Service(executable_path='C:/chromedriver.exe'))
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(url)
    with allure.step('Переход на страницу Регистрации'):
        time.sleep(1)
        browser.get(f"{base_url}/sign_up")
        WebDriverWait(browser, 10).until(
            EC.url_contains("/sign_up")
        )
    #time.sleep(2)
    with allure.step('Заполнение поля email'):
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        # EC.url_to_be()  #соответствие страницы на которую переходим
        # EC.presence_of_element_located() # проверяет наличие элемента в дереве дом (не надо ждать пока отрисуется)
        # EC.visibility_of_element_located() # проверяет видимость элемента и что пользователю виден
        email_field.send_keys(registration_data['email'])
        #browser.find_element(By.ID, "email").send_keys("myuser1@mail.ru")
    with allure.step('Заполнение поля name'):
        browser.find_element(By.ID, "username").send_keys(registration_data['name'])
    with allure.step('Заполнение поля password'):
        browser.find_element(By.ID, "pass1").send_keys(registration_data['password'])
    with allure.step('Подтверждение пароля'):
        browser.find_element(By.ID, "pass2").send_keys(registration_data['password'])

    with allure.step('Зарегистрироваться'):
        browser.find_element(By.CSS_SELECTOR, ".space-y-5>button").click()
    #time.sleep(5)
    with allure.step("Ожидаем страницу регистрации/авторизации"):
        #alert = browser.find_element(By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)")
        alert = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)"))
        )
        if alert.get_attribute("textContent") == "Вы успешно зарегистрировались. Теперь вы можете войти.":
            with allure.step("Ожидаем страницу авторизации"):
                wait.until(EC.url_to_be(f"{base_url}/login"))
                assert browser.current_url == "http://31.59.174.108/login"
        elif alert.get_attribute("textContent") == "email: user with this email already exists.":
            with allure.step("Ожидаем страницу регистрации"):
                wait.until(EC.url_to_be(f"{base_url}/sign_up"))
                assert browser.current_url == "http://31.59.174.108/sign_up"
        else:
            assert False, "Ошибка ожидаемых результатов"






    # assert browser.current_url == "http://31.59.174.108/login"
    # assert browser.current_url == "http://31.59.174.108/sign_up"
    # time.sleep(5)
    # alert = browser.find_element(By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)")
    # assert alert.get_attribute("textContent") == "Вы успешно зарегистрировались. Теперь вы можете войти." or alert.get_attribute("textContent") == "email: user with this email already exists."

    browser.quit()



@allure.epic("Аутентификация и авторизация")
@allure.feature("Регистрация пользователей")
@allure.suite("Смоук тесты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "ui")
@allure.label("owner", "QA - evgeny_gord")
@allure.id("TEST-123")
@allure.title("Проверка создания пользователя")
@allure.description("""
Этот тест проверяет:
- Регистрацию пользователя с позитивным сценарием
- Ввод рандомных значений с помощью библиотеки faker
- Проверка успеха прохождения регистрации 
ИЛИ
- Проверка предупреждения, что пользователь уже создан с таким email
""")
@allure.link("https://jira.example.com/TEST-123", name="JIRA Task")
@allure.issue("BUG-456", "https://bugtracker.com/BUG-456")
@allure.testcase("TC-789", "https://testcase.com/TC-789")
def test_positive_registration_faker(browser, base_url, wait, faker_data):
    #driver = webdriver.Chrome(service=Service(executable_path='C:/chromedriver.exe'))
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(url)
    with allure.step('Переход на страницу Регистрации'):
        time.sleep(1)
        browser.get(f"{base_url}/sign_up")
        WebDriverWait(browser, 10).until(
            EC.url_contains("/sign_up")
        )
    #time.sleep(2)

    with allure.step('Заполнение поля email'):
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        # EC.url_to_be()  #соответствие страницы на которую переходим
        # EC.presence_of_element_located() # проверяет наличие элемента в дереве дом (не надо ждать пока отрисуется)
        # EC.visibility_of_element_located() # проверяет видимость элемента и что пользователю виден
        email_field.send_keys(faker_data["email"])
        #browser.find_element(By.ID, "email").send_keys("myuser1@mail.ru")
    with allure.step('Заполнение поля name'):
        browser.find_element(By.ID, "username").send_keys(faker_data['name'])

    with allure.step('Заполнение поля password'):
        browser.find_element(By.ID, "pass1").send_keys(faker_data['password'])
        browser.find_element(By.ID, "pass2").send_keys(faker_data['password'])

    with allure.step('Зарегистрироваться'):
        browser.find_element(By.CSS_SELECTOR, ".space-y-5>button").click()

    with allure.step("Ожидаем страницу регистрации/авторизации"):
        alert = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)"))
        )
        if alert.get_attribute("textContent") == "Вы успешно зарегистрировались. Теперь вы можете войти.":
            with allure.step("Ожидаем страницу авторизации"):
                wait.until(EC.url_to_be(f"{base_url}/login"))
                assert browser.current_url == "http://31.59.174.108/login"
        elif alert.get_attribute("textContent") == "email: user with this email already exists.":
            with allure.step("Ожидаем страницу регистрации"):
                wait.until(EC.url_to_be(f"{base_url}/sign_up"))
                assert browser.current_url == "http://31.59.174.108/sign_up"
        else:
            assert False, "Ошибка ожидаемых результатов"

    browser.quit()


@allure.epic("Аутентификация и авторизация")
@allure.feature("Регистрация пользователей")
@allure.suite("Смоук тесты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "ui")
@allure.label("owner", "QA - evgeny_gord")
@allure.id("TEST-123")
@allure.title("Проверка создания пользователя")
@allure.description("""
Этот тест проверяет:
- Регистрацию пользователя с позитивным сценарием
- Прохождение регистрации на данных параметров фикстуры registration_data_with_params (хранится в test_ui/conftest.py)
- Проверка успеха прохождения регистрации 
ИЛИ
- Проверка предупреждения, что пользователь уже создан с таким email
""")
@allure.link("https://jira.example.com/TEST-123", name="JIRA Task")
@allure.issue("BUG-456", "https://bugtracker.com/BUG-456")
@allure.testcase("TC-789", "https://testcase.com/TC-789")
def test_positive_registration_with_fixture_params(browser, base_url, wait, registration_data_with_params):
    #driver = webdriver.Chrome(service=Service(executable_path='C:/chromedriver.exe'))
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(url)
    with allure.step('Переход на страницу Регистрации'):
        time.sleep(1)
        browser.get(f"{base_url}/sign_up")
        WebDriverWait(browser, 10).until(
            EC.url_contains("/sign_up")
        )
    #time.sleep(2)
    with allure.step('Заполнение поля email'):
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        # EC.url_to_be()  #соответствие страницы на которую переходим
        # EC.presence_of_element_located() # проверяет наличие элемента в дереве дом (не надо ждать пока отрисуется)
        # EC.visibility_of_element_located() # проверяет видимость элемента и что пользователю виден
        email_field.send_keys(registration_data_with_params['email'])
        #browser.find_element(By.ID, "email").send_keys("myuser1@mail.ru")
    with allure.step('Заполнение поля name'):
        browser.find_element(By.ID, "username").send_keys(registration_data_with_params['name'])

    with allure.step('Заполнение поля password'):
        browser.find_element(By.ID, "pass1").send_keys(registration_data_with_params['password'])
        browser.find_element(By.ID, "pass2").send_keys(registration_data_with_params['password'])

    with allure.step('Зарегистрироваться'):
        browser.find_element(By.CSS_SELECTOR, ".space-y-5>button").click()

    with allure.step("Ожидаем страницу регистрации/авторизации"):
        alert = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)"))
        )
        if alert.get_attribute("textContent") == "Вы успешно зарегистрировались. Теперь вы можете войти.":
            with allure.step("Ожидаем страницу авторизации"):
                wait.until(EC.url_to_be(f"{base_url}/login"))
                assert browser.current_url == "http://31.59.174.108/login"
        elif alert.get_attribute("textContent") == "email: user with this email already exists.":
            with allure.step("Ожидаем страницу регистрации"):
                wait.until(EC.url_to_be(f"{base_url}/sign_up"))
                assert browser.current_url == "http://31.59.174.108/sign_up"
        else:
            assert False, "Ошибка ожидаемых результатов"

    browser.quit()

    # pytest -v -k test_name --alluredir=allure-results --clean-alluredir

    # allure generate allure-results -o allure-report --clean

    # allure open allure-report
    # pytest -v test_first.py::test_positive_registration --alluredir=allure-results --clean-alluredir