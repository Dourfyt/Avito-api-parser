import os
import time
import re
from notifiers.logging import NotificationHandler
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
tickets = File("tg/tickets")

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

    import os

    @logger.catch
    def __parse_page(self):
        """Парсит открытую страницу"""
        time.sleep(1)
        try:
            # Читаем существующие ID из файла tickets.txt
            if os.path.isfile('tg/tickets.txt'):
                with open('tg/tickets.txt', 'r') as file:
                    # Очищаем каждый ID от лишних пробелов и символов
                    self.tickets_list = list(map(str.rstrip, file.readlines()))
            else:
                self.tickets_list = []

            navigator = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(Locator.NAVIGATOR))
            self.action.move_to_element(navigator)
            self.action.perform()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(Locator.LI_NAVIGATOR)).click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name=pagination-select]"))).click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.Custom-select-option__HLXYwVWDUc span")))
            options = self.driver.find_elements(By.CSS_SELECTOR, "div.Custom-select-option__HLXYwVWDUc span")
            for option in options:
                if option.text == "100":
                    option.click()
            time.sleep(1)

            # Парсим строки на странице и собираем ID в массив
            rows = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(Locator.ROWS))
            page_ids = []

            for row in rows:
                id_element = row.find_element(*Locator.ID)
                id_text = id_element.text.strip()  # Убираем пробелы
                status = str(row.find_element(*Locator.STATUS).text).lower()

                if id_text and status == "не запланировано":
                    page_ids.append(id_text)
                else:
                    continue
            # Проверяем каждый ID из файла и кликаем, если найден на странице
            for ticket_id in reversed(self.tickets_list):
                if ticket_id in page_ids:
                    try:
                        id_element = next(row.find_element(*Locator.ID) for row in rows if
                                          row.find_element(*Locator.ID).text.strip() == ticket_id)
                        id_element.click()
                        self.__parse_full_page(ticket_id)
                    except Exception as e:
                        print(f"Ошибка клика по ID: {ticket_id}, ошибка: {e}")
            self.tickets_list = [ticket_id for ticket_id in self.tickets_list if ticket_id in page_ids]

            with open('tg/tickets.txt', 'w') as file:
                for ticket_id in self.tickets_list:
                    file.write(f"{ticket_id}\n")

        except Exception as e:
            print(f"Ошибка при обработке: {e}")

    def __pretty_log(self, data):
        """Красивый вывод"""
        try:
            coef = data.get('coefficient')
            date = data.get('date')
            id_ticket = data.get('id_ticket')
            print(f"Ticket ID для удаления: {id_ticket}")
            logger.success(f'Статус заявки №{id_ticket} изменен на "запланирован" с коэффициентом {coef} | {date}')
            tickets.delete(str(id_ticket.strip()))
        except Exception as e:
            print(e)

    def __parse_full_page(self, url: str, data: dict = {}) -> bool:
        """Парсит для доп. информации открытое объявление на отдельной вкладке"""
        try:
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(Locator.PLAN)).click()
            cells = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(Locator.CELLS_TABLE))
            current_url = str(self.driver.current_url)
            id_ticket = current_url.split("&")[-2].split("=")[-1]

            for cell in cells:
                try:
                    date = cell.find_element(By.CSS_SELECTOR, "div.Calendar-cell__date-container__2TUSaIwaeG span").text
                    coefficient_element = cell.find_element(By.CSS_SELECTOR, "div.Coefficient-table-cell__EqV0w0Bye8")
                    coefficient_text = coefficient_element.text

                    if "Бесплатно" in coefficient_text:
                        coefficient_value = "Бесплатно"
                        button_hover = cell.find_element(By.CSS_SELECTOR,
                                                         'div.Calendar-cell__button-container__ANliSQlw9D')

                        # Перемещение курсора на кнопку
                        self.action.move_to_element(button_hover).perform()
                        time.sleep(1)

                        # Клик только при успешном нахождении элемента
                        try:
                            cell.find_element(By.XPATH, '//button[span[text()="Выбрать"]]').click()
                            self.__pretty_log({"id_ticket": id_ticket, 'coefficient': coefficient_value, 'date': date})
                            return True
                        except Exception as e:
                            print(f"Error clicking 'Выбрать': {e}")

                    elif '✕' in coefficient_text:
                        coefficient_value = coefficient_text.split('✕')[1].strip()
                        if coefficient_value == "1":
                            button_hover = cell.find_element(By.CSS_SELECTOR,
                                                             'div.Calendar-cell__button-container__ANliSQlw9D')

                            # Перемещение курсора на кнопку
                            self.action.move_to_element(button_hover).perform()
                            time.sleep(1)

                            # Клик только при успешном нахождении элемента
                            try:
                                cell.find_element(By.XPATH, '//button[span[text()="Выбрать"]]').click()
                                self.__pretty_log(
                                    {"id_ticket": id_ticket, 'coefficient': coefficient_value, 'date': date})
                                return True
                            except Exception as e:
                                print(f"Error clicking 'Выбрать': {e}")

                    else:
                        print("Коэффициент не найден")

                except Exception as e:
                    print(f"Ошибка: {e}")
                    continue

        except Exception as e:
            print(f"Ошибка: {e}")

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
    persons = config["BOT"]["PERSON"].split(",")
    for person in persons:
        if token and person:
            params = {
                'token': token,
                'chat_id': person
            }
            tg_handler = NotificationHandler("telegram", defaults=params)
            logger.add(tg_handler, level="SUCCESS", format="{message}")
    logger.success('Браузер запущен')
    try:
        while True:
            with webdriver.Chrome(options=options) as browser_driver:
                time.sleep(0.5)
            try:
                driver = WBParse(
                    url=url,
                    driver=browser_driver,
                    action = webdriver.ActionChains(browser_driver)
                )
                driver.parse()
                driver.driver.quit()
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