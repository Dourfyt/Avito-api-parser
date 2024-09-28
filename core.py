import os
import time
import re
from notifiers.logging import NotificationHandler
from seleniumbase import SB
from loguru import logger
from selenium.webdriver import ActionChains
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locator import Locator
import configparser
import json


config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")

class WBParse:

    def __init__(self,
                 driver = None,
                 url = None,
                 action = None,
                 ):
        self.data = []
        self.url = url
        self.tg_token = config['BOT']["TOKEN"]
        self.driver = driver
        self.action = action

    def __get_url(self):
        self.driver.get(self.url)
        time.sleep(5)
        
    @logger.catch
    def __parse_page(self):
        """Парсит открытую страницу"""
        time.sleep(1)
        try:
            if os.path.isfile('tg/tickets.txt'):
                with open('tg/tickets.txt', 'r') as file:
                    self.tickets_list = list(map(str.rstrip, file.readlines()))
            else:
                with open('tg/tickets.txt', 'w') as file:
                    self.tickets_list = []
            navigator = self.driver.find_element(*Locator.NAVIGATOR)
            self.action.move_to_element(navigator)
            self.action.perform()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(*Locator.LI_NAVIGATOR)
                ).click()
            rows = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(*Locator.ROWS))
            for row in rows:
                id = row.find_element(*Locator.ID)
                status = str(row.find_element(*Locator.STATUS).text)
                if id.text and status.lower() == "не запланировано":
                    if os.path.isfile('tg/tickets.txt'):
                        with open('tg/tickets.txt', 'r') as file:
                            self.tickets_list = list(map(str.rstrip, file.readlines()))
                            if len(self.tickets_list) > 5000:
                                self.tickets_list = self.tickets_list[-900:]
                    if self.is_tickets(id.text.strip()):
                        id.click()
                        self.__parse_full_page(id)
                        break
                    else:
                        continue
        except Exception as e:
            logger.error(f"Ошибка при обработке: {e}")

    def __pretty_log(self, id):
        """Красивый вывод"""
        logger.success(f'Статус заявки {id} изменен')

    def __parse_full_page(self, url: str, data: dict = {}) -> dict:
        """Парсит для доп. информации открытое объявление на отдельной вкладке"""
        time.sleep(1)
        try:
            self.driver.find_element(*Locator.PLAN).click()
            time.sleep(2)
            cells = self.driver.find_elements(*Locator.CELLS_TABLE)
            for cell in cells:
                try:
                    date = cell.find_element(By.CSS_SELECTOR, "div.Calendar-cell__date-container__2TUSaIwaeG span").text
                    coefficient_element = cell.find_element(By.CSS_SELECTOR,"div.Coefficient-table-cell__EqV0w0Bye8")
                    coefficient_text = coefficient_element.text
                    if "Бесплатно" in coefficient_text:
                        coefficient_value = "Бесплатно"
                        button_hover = cell.find_element(By.CSS_SELECTOR, 'div.Calendar-cell__button-container__ANliSQlw9D')
                        try:
                            self.action.move_to_element(button_hover)
                            self.action.perform()
                            time.sleep(1)
                            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Выбрать"]]'))
                            ).click()
                            return {'coefficient': coefficient_value, 'date':date,}
                        except Exception as e:
                            print(e)
                            continue
                    else:
                        if '✕' in coefficient_text:
                            coefficient_value = coefficient_text.split('✕')[1].strip()
                            if coefficient_value == "1":
                                button_hover = cell.find_element(By.CSS_SELECTOR, 'div.Calendar-cell__button-container__ANliSQlw9D')
                                try:
                                    self.action.move_to_element(button_hover)
                                    self.action.perform()
                                    time.sleep(1)
                                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Выбрать"]]'))
                                    ).click()
                                    return
                                except Exception as e:
                                    print(e)
                                    continue
                        else:
                            print("Коэффициент не найден")
                except Exception as e:
                    continue
        except:
            pass

        return data

    def is_tickets(self, id: str) -> bool:
        if id == self.tickets_list[-1]:
            return True
        return False

    def parse(self):
        """Метод для вызова парсинга"""
        try:
            self.__get_url()  # Загрузка страницы
            logger.info(f"Страница загружена")
            self.__parse_page()
            logger.info(f"Парсинг завершен")
        except Exception as error:
            logger.error(f"Ошибка при обработке: {error}")

def main():
    url = 'https://seller.wildberries.ru/supplies-managment/all-supplies'
    options = webdriver.ChromeOptions()
    options.add_argument(r'user-data-dir=usr\bin\User Data')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        with webdriver.Chrome(options=options) as browser_driver:
            time.sleep(0.5)
            while True:
                try:
                    driver = WBParse(
                        url=url,
                        driver=browser_driver,
                        action = webdriver.ActionChains(browser_driver)
                    )
                    driver.parse()
                    logger.info(f"Завершен парсинг для URL: {url}")
                except Exception as error:
                    logger.error(f"Ошибка при парсинге URL {url}: {error}")
                    logger.error('Произошла ошибка, но работа будет продолжена через 30 сек.')
                logger.info("Пауза перед следующим циклом")
                time.sleep(int(config["BOT"]["INTERVAL"])*60)
    except Exception as e:
        logger.error(f"Ошибка при создании браузера: {e}")


if __name__ == "__main__":
    main()