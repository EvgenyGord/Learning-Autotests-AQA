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




