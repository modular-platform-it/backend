import logging
from pathlib import Path


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования для этого логгера
        BASE_DIR = Path(__file__).resolve().parent.parent
        log_file = f"{BASE_DIR}/logger.log"
        formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)  # Добавляем обработчик файла к логгеру
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)  # Добавляем консольный обработчик к логгеру


# Создаем экземпляр Logger
py_logger = Logger(__name__)


def error_logger(func):
    """
    Декоратор, логирующий функции.
    Если во время выполнения декорируемой функции возникла ошибка,
    то в файл logger.log записываются ошибки
    """
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except Exception as e:
            py_logger.error(f"An error occurred: {str(e)}")

    return wrapper

