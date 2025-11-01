import pytest
from faker import Faker

@pytest.fixture
def api_url_petstore():
    return "https://petstore.swagger.io/v2"

@pytest.fixture
def api_url_demo_qa():
    return "https://demoqa.com"


@pytest.fixture
def faker_data():
    fake = Faker('ru_RU')
    return {
        "email": fake.ascii_free_email(),
        "name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": fake.password(length=8)
    }