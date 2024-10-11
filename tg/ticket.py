import os
from pathlib import Path

class File:
    def __init__(self, filename):
        self.filename = str(filename) + '.txt'
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self):
        if not os.path.exists(self.filename):
            with open(f"{Path(__file__).resolve().parent.parent}{self.filename}", "w") as f:
                pass

    def rewrite(self):
        with open(self.filename, "w") as f:
            return "Файл успешно сброшен!"

    def show(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
            result = ''
            if len(lines) > 0:
                for line in lines:
                    result += line
                return result
            else:
                return "Файл пустой"

    def add(self, ticket_id, max_rate):
        """Добавить строку заявки с максимальным коэффициентом"""
        with open(self.filename, "a") as f:
            f.write(f"{ticket_id}:{max_rate}\n")

    def get(self, ticket_id):
        """Получить строку заявки с коэффициентом по id"""
        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.split(':')[0].strip() == str(ticket_id):
                    return line.strip()  # Возвращает строку в формате id_заявки:макс_коэффициент
            return "Заявка не найдена"

    def get_first(self):
        """Получить первую строку заявки с коэффициентом"""
        with open(self.filename, "r") as f:
            return f.readline().strip()

    def delete_first(self):
        """Удалить первую строку заявки"""
        with open(self.filename, "r") as f:
            lines = f.readlines()
        with open(self.filename, "w") as f:
            for line in lines[1:]:
                f.write(line)

    def delete(self, ticket_id):
        """Удалить заявку по id"""
        found = False
        ticket_id = str(ticket_id).strip()
        with open(self.filename, "r") as f:
            lines = f.readlines()

        with open(self.filename, "w") as f:
            for line in lines:
                if line.split(':')[0].strip() != ticket_id:
                    f.write(line)
                else:
                    found = True

        if not found:
            return "Заявка не найдена"
