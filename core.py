import os
import time
import re
import requests
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
from tg.ticket import File


config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")
tickets = File("tickets.txt")

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

            navigator = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(Locator.NAVIGATOR))
            self.action.move_to_element(navigator)
            self.action.perform()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(Locator.LI_NAVIGATOR)).click()
            rows = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(Locator.ROWS))
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
                        id_ticket = id
                        id.click()
                        if self.__parse_full_page(id):
                            tickets.delete(id_ticket.text.strip())
                            break
                    else:
                        continue
        except Exception as e:
            print(f"Ошибка при обработке: {e}")

    def __pretty_log(self, data):
        """Красивый вывод"""
        try:
            coef = data.get('coefficient')
            date = data.get('date')
            id_ticket = data.get('id_ticket')
            logger.success(f'Статус заявки №{id_ticket} изменен на "запланирован" с коэффициентом {coef} | {date}')
        except Exception as e:
            print(e)


    def __parse_full_page(self, url: str, data: dict = {}) -> bool:
        """Парсит для доп. информации открытое объявление на отдельной вкладке"""
        try:
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(Locator.PLAN)).click()
            cells = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(Locator.CELLS_TABLE))
            for cell in cells:
                try:
                    current_url = str(self.driver.current_url)
                    id_ticket = current_url.split("&")[-2]
                    print(id_ticket)
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
                            cell.find_element(By.XPATH, '//button[span[text()="Выбрать"]]').click()
                            self.__pretty_log({"id_ticket":id_ticket,'coefficient': coefficient_value, 'date':date})
                            return True
                        except Exception as e:
                            cell.find_element(By.XPATH, '//button[span[text()="Выбрать"]]').click()
                            self.__pretty_log({"id_ticket":id_ticket,'coefficient': coefficient_value, 'date':date})
                    else:
                        if '✕' in coefficient_text:
                            coefficient_value = coefficient_text.split('✕')[1].strip()
                            date = cell.find_element(By.CSS_SELECTOR,"div.Calendar-cell__date-container__2TUSaIwaeG span").text
                            if coefficient_value == "1":
                                button_hover = cell.find_element(By.CSS_SELECTOR, 'div.Calendar-cell__button-container__ANliSQlw9D')
                                try:
                                    self.action.move_to_element(button_hover)
                                    self.action.perform()
                                    time.sleep(1)
                                    cell.find_element(By.XPATH, '//button[span[text()="Выбрать"]]').click()
                                    self.__pretty_log({"id_ticket":id_ticket,'coefficient': coefficient_value, 'date':date})
                                    return True
                                except Exception as e:
                                    cell.find_element(By.XPATH, '//button[span[text()="Выбрать"]]').click()
                                    self.__pretty_log({"id_ticket":id_ticket,'coefficient': coefficient_value, 'date':date})
                                    return
                        else:
                            print("Коэффициент не найден")
                except Exception as e:
                    continue
        except:
            pass
        return False

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
            print(f"Ошибка при обработке: {error}")

def main():
    url = 'https://seller.wildberries.ru/supplies-managment/all-supplies'
    options = webdriver.ChromeOptions()
    options.add_argument(r'user-data-dir=usr\bin\User Data')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    token = config["BOT"]["TOKEN"]
    person = config["BOT"]["PERSON"]
    if token and person:
        params = {
            'token': token,
            'chat_id': person
        }
        tg_handler = NotificationHandler("telegram", defaults=params)
        logger.add(tg_handler, level="SUCCESS", format="{message}")
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
                    print(f"Ошибка при парсинге URL {url}: {error}")
                    print('Произошла ошибка, но работа будет продолжена через 30 сек.')
                logger.info("Пауза перед следующим циклом")
                time.sleep(int(config["BOT"]["INTERVAL"])*60)
    except Exception as e:
        print(f"Ошибка при создании браузера: {e}")


if __name__ == "__main__":
    main()