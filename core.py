import os
import time
from notifiers.logging import NotificationHandler
from loguru import logger
from selenium.webdriver import ActionChains
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locator import Locator
import configparser
import locale
from datetime import datetime, timedelta
from tg.ticket import File

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

is_empty = False

#Читаем конфиг, файл с поставками
config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")
tickets = File("tg/tickets")

def delay():
    time.sleep(int(config["BOT"]["DELAY"]))

class WBParse:
    """Класс парсера"""
    def __init__(self,
                 driver = None,
                 url = None,
                 action = None,
                 ):
        self.url = url
        self.driver = driver
        self.action = action

    def __get_url(self):
        self.driver.get(self.url)
        time.sleep(5)

    @logger.catch
    def __parse_page(self):
        """Парсит все поставки"""
        time.sleep(1)
        delay()
        global is_empty
        try:
            # Читаем существующие ID из файла tickets.txt
            if os.path.isfile('tg/tickets.txt'):
                with open('tg/tickets.txt', 'r') as file:
                    # Очищаем каждый ID от лишних пробелов и символов
                    self.tickets_list = list(map(str.rstrip, file.readlines()))
            else:
                self.tickets_list = []
            if len(self.tickets_list) != 0:
                is_empty = False
                self.__get_to_postavki()
                try:
                    self.__pagination()
                except:
                    print("Пагинация не удалась")
                time.sleep(5)
                delay()
                # Парсим строки на странице и собираем ID в массив
                try:
                    rows = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(Locator.ROWS))
                except:
                    print("Не удалось спарсить строки")
                page_ids = []
                delay()
                for row in rows:
                    try:
                        id_element = row.find_element(*Locator.ID)
                    except:
                        print("ID не найден на 76 строке")
                    id_text = id_element.text.strip()  # Убираем пробелы
                    status = str(row.find_element(*Locator.STATUS).text).strip().lower()
                    if id_text and status == "не запланировано":
                        page_ids.append(id_text)
                    else:
                        continue
                logger.info(f"Заявки на странице: {page_ids}")

                # Проверяем каждый ID из файла и кликаем, если найден на странице
                for ticket in reversed(self.tickets_list):
                    ticket_id = ticket.split(":")[0]
                    if ticket_id in page_ids:
                        try:
                            rows = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(Locator.ROWS))
                            try:
                                id_element = next(row.find_element(*Locator.ID) for row in rows if row.find_element(*Locator.ID).text.strip() == ticket_id)
                            except:
                                print(f"ID {ticket_id} не найден на в строке.")
                                continue
                            id_element.click()
                            self.__parse_full_page(ticket_id)
                            delay()
                            self.__get_url()
                            self.__get_to_postavki()
                            self.__pagination()
                            time.sleep(int(config["BOT"]["IN_CYCLE_DELAY"])*60)
                        except Exception as e:
                            print(f"Ошибка клика по ID: {ticket_id}, ошибка: {e}")
                logger.info(f"Текущие заявки из файла: {self.tickets_list}")
                self.tickets_list = [ticket_id for ticket_id in self.tickets_list if ticket_id.split(":")[0] in page_ids]
                logger.info(f"Текущие заявки из файла после проверки: {self.tickets_list}")
                with open('tg/tickets.txt', 'w') as file:
                    for ticket_id in self.tickets_list:
                        file.write(f"{ticket_id}\n")
            elif not is_empty:
                is_empty = True
                logger.success("Все заявки отработаны - файл пустой")

        except Exception as e:
            print(f"Ошибка при обработке в __parse_page: {e}")

    def __pagination(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(Locator.PAGINATION)).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(Locator.OPTIONS))
        options = self.driver.find_elements(*Locator.OPTIONS)
        for option in options:
            if option.text == "100":
                option.click()

    def __get_to_postavki(self):
        navigator = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(Locator.NAVIGATOR))
        self.action.move_to_element(navigator)
        self.action.perform()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(Locator.LI_NAVIGATOR)).click()

    def __pretty_log(self, data):
        """Уведомление в бота"""
        try:
            coef = data.get('coefficient')
            date = data.get('date')
            id_ticket = data.get('id_ticket')
            new_id = data.get("new_id")
            new_id = new_id.split(' ')[1]
            print(f"Ticket ID для удаления: {id_ticket}")
            logger.success(f'Статус заявки №{id_ticket} изменен на "запланирован" с коэффициентом {coef} | {date}\n\nНомер поставки изменен на: №{new_id}')
            tickets.delete(str(id_ticket.strip()))
        except Exception as e:
            print("Ошибка при уведомлении в ТГ - ",e)

    def __parse_full_page(self, url: str, data: dict = {}) -> bool:
        """Парсит поставку с проверкой коэффициентов от 'Бесплатно' до максимального"""
        try:
            time.sleep(1)
            delay()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(Locator.PLAN)).click()
            cells = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(Locator.CELLS_TABLE))
            current_url = str(self.driver.current_url)
            id_ticket = current_url.split("&")[-2].split("=")[-1]
            button_planning = self.driver.find_element(*Locator.CONFIRM)

            ticket_data = tickets.get(id_ticket)

            if ticket_data != "Заявка не найдена":
                _, max_rate = ticket_data.split(':')
                max_rate = int(max_rate)
            else: max_rate = 0

            coefficients = ["Бесплатно"] + [f'✕{i}' for i in range(1, max_rate + 1)]
            
            for coefficient in coefficients:
                for cell in cells:
                    try:
                        date_text = cell.find_element(*Locator.DATE).text
                        try:
                            date_text_clean = date_text.split(',')[0].strip()
                            date_object = datetime.strptime(date_text_clean, "%d %B")
                            date_object = date_object.replace(year=datetime.now().year)
                        except ValueError as ve:
                            print(f"Ошибка при преобразовании даты: {ve}")
                            continue

                        buffer_days = int(config["BOT"]["BUFFER"])
                        today = datetime.now()
                        buffer_date = today + timedelta(days=buffer_days)

                        if date_object > buffer_date:
                            coefficient_element = cell.find_element(*Locator.RATE)
                            coefficient_text = coefficient_element.text
                            if coefficient_text.strip() == f"{coefficient}":
                                button_hover = cell.find_element(*Locator.CHOOSE_HOVER)
                                self.action.move_to_element(button_hover).perform()
                                time.sleep(1)
                                try:
                                    cell.find_element(*Locator.CHOOSE).click()
                                    time.sleep(2)
                                    self.action.move_to_element(button_planning).click().perform()
                                    time.sleep(10)
                                    new_id_el = self.driver.find_element(*Locator.ID).text
                                    new_id = new_id_el.strip()
                                    time.sleep(1)
                                    logger.debug("ЗАЯВКА ПРОШЛА")
                                    self.__pretty_log({"id_ticket": id_ticket, 'coefficient': coefficient, 'date': date_text, "new_id": new_id})
                                    return True
                                except Exception as e:
                                    print(f"Ошибка при нажатии 'Выбрать': {e}")
                            else:
                                continue

                        else:
                            continue

                    except Exception as e:
                        print(f"Ошибка: {e}")
                        continue

        except Exception as e:
            print(f"Ошибка: {e}")

        return False

    def is_tickets(self, id: str) -> bool:
        """Есть ли заявка в файле"""
        if id == self.tickets_list:
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

    #Добавляем уведомления каждому пользователю
    for person in persons:
        if token and person:
            params = {
                'token': token,
                'chat_id': person
            }
            tg_handler = NotificationHandler("telegram", defaults=params)
            logger.add(tg_handler, level="SUCCESS", format="{message}")

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