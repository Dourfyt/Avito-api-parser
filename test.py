import json
from seleniumwire import webdriver  # Используем Selenium Wire вместо стандартного Selenium
import time
def main():
    url = 'https://seller.wildberries.ru/supplies-management/all-supplies'

    # Опции для Chrome
    options = webdriver.ChromeOptions()
    options.add_argument(r'user-data-dir=usr\bin\User Data')
    options.add_argument('--profile-directory=Profile 1')
    # Настройка заголовков
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Upgrade-Insecure-Requests": "1",
        "sec-ch-ua-platform": "Linux",
        "sec-ch-ua-mobile": "?0"
    }

        # Создаём WebDriver с Selenium Wire
    with webdriver.Chrome(options=options) as browser_driver:

        browser_driver.get(url)

        time.sleep(20)
        # Обновляем страницу
        browser_driver.refresh()

        time.sleep(20)
        # Добавьте здесь свои дальнейшие действия с браузером
if __name__ == "__main__":
    main()
