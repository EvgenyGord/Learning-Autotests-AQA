import pytest


@pytest.fixture
def api_url_petstore():
    return "https://petstore.swagger.io/v2"

@pytest.fixture
def api_url_demo_qa():
    return "https://demoqa.com"
