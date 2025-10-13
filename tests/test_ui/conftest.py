import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    # тест побежал, что-то делает, что-то сделал
    driver.quit()


# driver = webdriver.Chrome()
# driver.get(url)
# time.sleep(3)
# driver.quit()

# @pytest.fixture
# def browser(request):
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--window-size=1920,1080')
#     driver = webdriver.Chrome(options=options)
# #   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     request.node.driver = driver
#     yield driver
#     driver.quit()


@pytest.fixture
def base_url():
    return "http://31.59.174.108"



@pytest.fixture(params=[
    {"email": "test2@mail.ru",
     "name": "User25",
     "password": "qwertyu1"},
    {"email": "test3@mail.ru",
     "name": "User26",
     "password": "qwertyu2"},
    {"email": "test4@mail.ru",
     "name": "User27",
     "password": "qwertyu3"}
])
def registration_data_with_params(request):
    return request.param


@pytest.fixture
def registration_data():
    return {
        "email": "test_user123@mail.ru",
        "name": "User25",
        "password": "qwertyui"
    }



@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.positive
@pytest.mark.regression
@pytest.mark.fixture
@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)



@pytest.fixture
def faker_data():
    fake = Faker('ru_RU')
    return {
        "email": fake.ascii_free_email(),
        "name": fake.first_name(),
        "password": fake.password(length=8)
    }



# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#
#     if rep.when == "call" and rep.failed:
#         driver = getattr(item._request.node, "driver", None)
#         if driver:
#             os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
#             timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
#             screenshot_path = os.path.join(SCREENSHOTS_DIR, f"screenshot_{timestamp}.png")
#
#             driver.save_screenshot(screenshot_path)
#
#             with open(screenshot_path, "rb") as image_file:
#                 allure.attach(image_file.read(), name=f"Screenshot {timestamp}", attachment_type=AttachmentType.PNG)
#

# удалить старые скриншоты
# @pytest.fixture(scope="session", autouse=True)
# def clean_screenshots_before_tests():
#     if os.path.exists(SCREENSHOTS_DIR):
#         for filename in os.listdir(SCREENSHOTS_DIR):
#             file_path = os.path.join(SCREENSHOTS_DIR, filename)
#             try:
#                 if os.path.isfile(file_path):
#                     os.remove(file_path)
#             except Exception as e:
#                 print(f"не удалить файл {file_path}: {e}")
#     else:
#         os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def pytest_runtest_setup(item):
    # Этот хук будет вызван перед запуском КАЖДОГО теста
    print(f">>> Начинается выполнение теста: {item.name}")