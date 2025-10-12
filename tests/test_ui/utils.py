import allure
import os
import time
from functools import wraps


def screenshot_on_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            browser = kwargs.get('browser') or args[0]
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            # os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")

            browser.save_screenshot(screenshot_path)

            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Screenshot {timestamp}",
                    attachment_type=allure.attachment_type.PNG
                )

            raise
    return wrapper
