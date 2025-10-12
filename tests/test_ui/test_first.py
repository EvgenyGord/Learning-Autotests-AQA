import time
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



def test_positive_registration(browser, base_url, wait, registration_data):
    #driver = webdriver.Chrome(service=Service(executable_path='C:/chromedriver.exe'))
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(url)
    browser.get(f"{base_url}/sign_up")
    #time.sleep(2)
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    # EC.url_to_be()  #соответствие страницы на которую переходим
    # EC.presence_of_element_located() # проверяет наличие элемента в дереве дом (не надо ждать пока отрисуется)
    # EC.visibility_of_element_located() # проверяет видимость элемента и что пользователю виден
    email_field.send_keys(registration_data['email'])
    #browser.find_element(By.ID, "email").send_keys("myuser1@mail.ru")
    browser.find_element(By.ID, "username").send_keys(registration_data['name'])
    browser.find_element(By.ID, "pass1").send_keys(registration_data['password'])
    browser.find_element(By.ID, "pass2").send_keys(registration_data['password'])


    browser.find_element(By.CSS_SELECTOR, ".space-y-5>button").click()

    wait.until(EC.url_to_be(f"{base_url}/sign_up"))

    assert browser.current_url == "http://95.182.122.183/sign_up"
    time.sleep(5)
    alert = browser.find_element(By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)")
    assert alert.get_attribute("textContent") == "Что-то пошло не так. Пожалуйста, попробуйте позже"

    browser.quit()




def test_positive_registration_faker(browser, base_url, wait, faker_data):
    #driver = webdriver.Chrome(service=Service(executable_path='C:/chromedriver.exe'))
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(url)
    browser.get(f"{base_url}/sign_up")
    #time.sleep(2)
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    # EC.url_to_be()  #соответствие страницы на которую переходим
    # EC.presence_of_element_located() # проверяет наличие элемента в дереве дом (не надо ждать пока отрисуется)
    # EC.visibility_of_element_located() # проверяет видимость элемента и что пользователю виден
    email_field.send_keys(faker_data["email"])
    #browser.find_element(By.ID, "email").send_keys("myuser1@mail.ru")
    browser.find_element(By.ID, "username").send_keys(faker_data['name'])
    browser.find_element(By.ID, "pass1").send_keys(faker_data['password'])
    browser.find_element(By.ID, "pass2").send_keys(faker_data['password'])


    browser.find_element(By.CSS_SELECTOR, ".space-y-5>button").click()

    wait.until(EC.url_to_be(f"{base_url}/sign_up"))

    assert browser.current_url == "http://95.182.122.183/sign_up"
    time.sleep(5)
    alert = browser.find_element(By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)")
    assert alert.get_attribute("textContent") == "Что-то пошло не так. Пожалуйста, попробуйте позже"

    browser.quit()



def test_positive_registration_with_fixture_params(browser, base_url, wait, registration_data_with_params):
    #driver = webdriver.Chrome(service=Service(executable_path='C:/chromedriver.exe'))
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(url)
    browser.get(f"{base_url}/sign_up")
    #time.sleep(2)
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    # EC.url_to_be()  #соответствие страницы на которую переходим
    # EC.presence_of_element_located() # проверяет наличие элемента в дереве дом (не надо ждать пока отрисуется)
    # EC.visibility_of_element_located() # проверяет видимость элемента и что пользователю виден
    email_field.send_keys(registration_data_with_params['email'])
    #browser.find_element(By.ID, "email").send_keys("myuser1@mail.ru")
    browser.find_element(By.ID, "username").send_keys(registration_data_with_params['name'])
    browser.find_element(By.ID, "pass1").send_keys(registration_data_with_params['password'])
    browser.find_element(By.ID, "pass2").send_keys(registration_data_with_params['password'])


    browser.find_element(By.CSS_SELECTOR, ".space-y-5>button").click()

    wait.until(EC.url_to_be(f"{base_url}/sign_up"))

    assert browser.current_url == "http://95.182.122.183/sign_up"
    time.sleep(5)
    alert = browser.find_element(By.CSS_SELECTOR, ".Toastify__toast-body>div:nth-child(2)")
    assert alert.get_attribute("textContent") == "Что-то пошло не так. Пожалуйста, попробуйте позже"

    browser.quit()

    # pytest -v -k test_name --alluredir=allure-results --clean-alluredir

    # allure generate allure-results -o allure-report --clean

    # allure open allure-report