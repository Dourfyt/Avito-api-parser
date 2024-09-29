import os
from pathlib import Path

class File:
    def __init__(self,filename):
        self.filename = str(filename)+'.txt'
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self):
        if not os.path.exists(self.filename):
            with open(f"{Path(__file__).resolve().parent.parent}{self.filename}", "w") as f:
                pass

    def show(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
            result = ''
            for line in lines:
                result += line
            return result


    def add(self, message):
        """Добавить строку"""
        with open(self.filename, "a") as f:
            f.write(message+'\n')

    def get(self, message):
        """Получить строку"""
        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip('\n') == message.text:
                    return line
                else: return "Данная строка не найдена"

    def get_first(self):
        """Получить первую строку"""
        with open(self.filename, "r") as f:
            return f.readline()
        
    def delete_first(self):
        """Удалить первую строку"""
        with open(self.filename, "r") as f:
            lines = f.readlines()
        with open(self.filename, "w") as f:
            for line in lines[1:]:
                    f.write(line)

    def delete(self, text):
        """Удалить строку"""
        found = False
        text = str(text).strip()  # Удаляем пробелы и символы новой строки у текста
        with open(self.filename, "r") as f:
            lines = f.readlines()

        with open(self.filename, "w") as f:
            for line in lines:
                if line.strip() != text:  # Удаляем пробелы и символы новой строки у строки файла
                    f.write(line)
                else:
                    found = True

        if not found:
            return "Данная строка не найдена"
