import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_simple_form_registration(browser, base_url_web_sandbox, wait):

    with allure.step("Ввод Username"):
        browser.get(f"{base_url_web_sandbox}")
        WebDriverWait(browser, 10).until(
            EC.url_to_be(base_url_web_sandbox))
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

    form_result = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#formResult>div>p")))
    assert 'Форма успешно отправлена!' in form_result.text
    time.sleep(5)





