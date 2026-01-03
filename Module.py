# Импорт стандартного модуля для работы с JSON
import json  # будем читать data.json и schema.json

# Импорт модуля логирования для записи ошибок в файл
import logging  # настроим лог-файл validation.log

# Импорт функций из библиотеки jsonschema для проверки данных по схеме
from jsonschema import validate
from jsonschema.exceptions import ValidationError

logging.basicConfig(
    filename="validation.log",  # лог-файл в папке с программой
    level=logging.INFO,  # записываем только ошибки и выше
    format="%(asctime)s - %(levelname)s - %(message)s",  # время, уровень, текст
)


def load_json(filepath: str):
    """
    Читает JSON-файл и возвращает данные как Python-объект.
    В случае ошибки пишет сообщение в лог и возвращает None.
    При успешном чтении пишет информационное сообщение.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # логируем успешное чтение
        logging.info(f"Файл успешно прочитан: {filepath}")
        return data

    except FileNotFoundError:
        logging.error(f"Файл не найден: {filepath}")
        return None

    except json.JSONDecodeError as e:
        logging.error(
            f"Ошибка разбора JSON в файле {filepath}: "
            f"{e.msg} (строка {e.lineno}, колонка {e.colno})"
        )
        return None

    except Exception as e:
        logging.error(f"Неизвестная ошибка при чтении файла {filepath}: {e}")
        return None


def validate_data(data, schema) -> bool:
    """
    Проверяет данные по JSON-схеме.
    Возвращает True, если данные валидны, иначе False.
    Все ошибки валидации пишутся в лог.
    """
    try:
        # Пытаемся провалидировать данные по схеме
        validate(instance=data, schema=schema)

        # Если исключения не было — данные валидны
        logging.info("Валидация прошла успешно")
        return True

    except ValidationError as e:
        # Ошибка несоответствия данным схеме
        logging.error(
            "Ошибка валидации JSON: %s | Путь в данных: %s",
            e.message,
            list(
                e.path
            ),  # путь до проблемного поля, превращаем в список для наглядности
        )
        return False

    except Exception as e:
        # Непредвиденная ошибка при валидации (например, неверная схема)
        logging.error(f"Неизвестная ошибка при валидации JSON: {e}")
        return False


def main():
    # 1. Читаем данные и схему из файлов
    data = load_json("data.json")
    schema = load_json("schema.json")

    # Если что-то не удалось прочитать (None) — прерываемся
    if data is None or schema is None:
        logging.error("Данные или схема не были загружены, валидация невозможна")
        return

    # 2. Валидируем данные по схеме
    is_valid = validate_data(data, schema)

    # 3. По желанию можно что-то вывести в консоль
    if is_valid:
        print("Данные валидны по схеме")
    else:
        print("Данные НЕ соответствуют схеме, подробности см. в лог-файле")


if __name__ == "__main__":
    main()
