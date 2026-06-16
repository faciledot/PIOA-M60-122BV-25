from .backend.memory import MidiKeyboardDB
from .backend.file import FileMidiKeyboardDB


db = None


def _init_database():
    global db
    print("Выберите тип базы данных:")
    print("1. In-memory")
    print("2. Файловая")
    choice = input("Введите номер: ").strip()
    if choice == "2":
        db = FileMidiKeyboardDB()
    else:
        db = MidiKeyboardDB()


def _print_menu() -> None:
    print("\n=== База MIDI-клавиатур ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("0. Выход")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")


def _read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите число.")


def _add_keyboard() -> None:
    print("\nДобавление записи")

    keyboard_id = _read_int("id: ")
    company_name = input("company_name: ").strip()
    keys_number = _read_int("keys_number: ")
    price = _read_float("price: ")
    has_pads = input("has_pads (да/нет): ").strip()

    try:
        record = db.create(keyboard_id, company_name, keys_number, price, has_pads)
        print(f"Запись добавлена: {record}")
    except Exception as exc:
        print(f"Ошибка: {exc}")


def _print_records(records: list[tuple[int, str, int, float, bool]]) -> None:
    if not records:
        print("Записи не найдены.")
        return
    for record in records:
        print(record)


def _show_all_keyboards() -> None:
    print("\nСписок записей")
    _print_records(db.select())


def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _read_optional_float(prompt: str) -> float | None:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите число или оставьте поле пустым.")


def _find_keyboards_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")
    keyboard_id = _read_optional_int("id: ")
    company_name = input("company_name: ").strip() or None
    keys_number = _read_optional_int("keys_number: ")
    price = _read_optional_float("price: ")
    has_pads = input("has_pads (да/нет): ").strip() or None

    records = db.select(
        keyboard_id=keyboard_id,
        company_name=company_name,
        keys_number=keys_number,
        price=price,
        has_pads=has_pads,
    )
    _print_records(records)


def run() -> None:
    _init_database()
    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()

        if action == "1":
            _add_keyboard()
        elif action == "2":
            _show_all_keyboards()
        elif action == "3":
            _find_keyboards_by_filter()
        elif action == "0":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")