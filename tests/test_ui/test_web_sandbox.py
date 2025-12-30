"""
Покрытие UI тестами различные формы
WEB Sandbox
https://aqa-proka4.org/sandbox/web#forms
"""


import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_simple_form_registration(browser, base_url_web_sandbox, wait):

    with allure.step("Переход на страницу с формами"):
        browser.get(f"{base_url_web_sandbox}")
        WebDriverWait(browser, 10).until(
            EC.url_to_be(base_url_web_sandbox))

    with allure.step("Ввод Username"):
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("evgeny_gord")

    with allure.step("Ввод email"):
        wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("evgeny_gord@mail.ru")

    with allure.step("Ввод password"):
        wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("qwerty123")

    with allure.step("Выбор Country"):
        wait.until(EC.visibility_of_element_located((By.ID, "country"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#country>[value='ru']"))).click()

    with allure.step("Соглашение с условиями регистрации"):
        wait.until(EC.visibility_of_element_located((By.ID, "terms"))).click()

    with allure.step("Нажатие на кнопку Регистрации"):
        wait.until(EC.visibility_of_element_located((By.ID, "submitBtn"))).click()

    with allure.step("Отправка формы на проверку, подтверждение успешной отправки"):
        form_result = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#formResult>div>p")))
        assert 'Форма успешно отправлена!' in form_result.text


def test_form_with_validation(browser, base_url_web_sandbox, wait):
    with allure.step("Переход на страницу с формами"):
        browser.get(f"{base_url_web_sandbox}")
        WebDriverWait(browser, 10).until(
            EC.url_to_be(base_url_web_sandbox))

    with allure.step("Ввод Usrname (минимум 5 символов)"):
        with allure.step("Проверка валидации поля, негатив"):
            with allure.step("Ввод некорректного username"):
                username = wait.until(EC.visibility_of_element_located((By.NAME, "val-username")))
                username.send_keys("test")
            with allure.step("Нажатие на кнопку, чтобы вызвать проверку валидации username"):
                button = wait.until(EC.visibility_of_element_located((By.ID, "valSubmitBtn")))
                button.click()
            with allure.step("Проверка текста валидации"):
                username_error = wait.until(EC.visibility_of_element_located((By.ID, "username-error"))).text
                assert username_error == "Username должен содержать минимум 5 символов"

        with allure.step("Заполнение корректного username >=5 символов"):
            username.clear()
            username.send_keys("Username")

    with allure.step("Ввод Email (должен содержать @)"):
        with allure.step("Проверка валидации поля, негатив"):
            with allure.step("Ввод некорректного email"):
                email = wait.until(EC.visibility_of_element_located((By.ID, "val-email")))
                email.send_keys("test.mail.ru")
            with allure.step("Нажатие на кнопку, чтобы вызвать проверку валидации"):
                button.click()
            with allure.step("Проверка текста валидации поля email"):
                email_error = wait.until(EC.visibility_of_element_located((By.ID, "email-error"))).text
                assert email_error == "Email должен содержать символ @"

            with allure.step("Заполнение корректного email (содержит символ @)"):
                email.clear()
                email.send_keys("test@mail.ru")

    with allure.step("Ввод Password (минимум 8 символов, буквы и цифры)"):
        with allure.step("Проверка валидации поля, негатив"):
            with allure.step("Ввод некорректного password"):
                password = wait.until(EC.visibility_of_element_located((By.ID, "val-password")))
                password.send_keys("qwerty1")
            with allure.step("Нажатие на кнопку, чтобы вызвать проверку валидации"):
                button.click()
            with allure.step("Проверка текста валидации поля password"):
                password_error = wait.until(EC.visibility_of_element_located((By.ID, "password-error"))).text
                assert password_error == "Password должен содержать минимум 8 символов, включая буквы и цифры"

            with allure.step("Заполнение корректного Password (содержит символ @)"):
                password.clear()
                password.send_keys("qwerty123")

    with allure.step("Подтверждение Password"):
        with allure.step("Проверка валидации поля, негатив"):
            with allure.step("Ввод некорректного password, который не совпадает"):
                confirm_password = wait.until(EC.visibility_of_element_located((By.ID, "val-confirm-password")))
                confirm_password.send_keys("qwerty1")
            with allure.step("Нажатие на кнопку, чтобы вызвать проверку валидации"):
                button.click()
            with allure.step("Проверка текста валидации поля password"):
                confirm_password_error = wait.until(EC.visibility_of_element_located((By.ID, "confirm-password-error"))).text
                assert confirm_password_error == "Пароли не совпадают"

            with allure.step("Заполнение корректного Password для подтверждения"):
                confirm_password.clear()
                confirm_password.send_keys("qwerty123")

    with allure.step("Проверить и отправить все"):
        button.click()
        form_result = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#valFormResult>div>p"))).text
        assert form_result == "Все проверки пройдены! Форма валидна."


def test_dinamic_form(browser, base_url_web_sandbox, wait):
    with allure.step("Позитивный сценарий (основной флоу с отправкой)"):
        with allure.step("Переход на страницу с формами"):
            browser.get(f"{base_url_web_sandbox}")
            WebDriverWait(browser, 10).until(
                EC.url_to_be(base_url_web_sandbox))

        with allure.step("Ввод имени"):
            wait.until(EC.visibility_of_element_located((By.ID, "dyn-name"))).send_keys("Евгений")

        with allure.step("Заполнение Email адреса"):
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//*[@name='email[]'])[1]"))).send_keys("evgeny_gord@mail.ru")

        with allure.step("Заполнение Номера телефонов"):
            wait.until(EC.visibility_of_element_located((By.NAME, "phone[]"))).send_keys("+79999999999")

        with allure.step("Отправка формы"):
            wait.until(EC.visibility_of_element_located((By.ID, "dynSubmitBtn"))).click()

    with allure.step("Доп. сценарии с формой"):
        with allure.step("Удаление поля email, когда один элемент"):
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[onclick='removeEmailField(this)']"))).click()
            alert = wait.until(EC.alert_is_present())
            assert alert.text == "Должен остаться хотя бы один email!"
            alert.accept()
        with allure.step("Добавление нового email"):
            with allure.step("Добавление нового поля"):
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[onclick='addEmailField()']"))).click()
            with allure.step("Заполнение нового email"):
                wait.until(EC.visibility_of_element_located((By.XPATH, "(//*[@name='email[]'])[2]"))).send_keys("test2.0@mail.ru")















