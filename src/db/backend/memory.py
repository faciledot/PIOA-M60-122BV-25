
type MidiKeyboardRecord = tuple[int, str, int, float, bool]

MidiKeyboard: list[MidiKeyboardRecord] = []

def create_record(
    keyboard_id: int,
    company_name: str,
    keys_number: int,
    price: float,
    has_pads: str,
) -> MidiKeyboardRecord:
    if keys_number <= 0:
        raise ValueError("Поле keys_number не может быть отрицательным или нулевым.")
    if keys_number > 88:
        raise ValueError("Количество клавиш не может превышать 88.")

    if price < 0:
        raise ValueError("Поле price не может быть отрицательным.")

    if has_pads.strip().lower() not in ("да", "нет"):
        raise ValueError("Поле has_pads должно принимать значения 'да' или 'нет'.")

    if any(record[0] == keyboard_id for record in MidiKeyboard):
        raise ValueError(f"Запись с id={keyboard_id} уже существует.")

    new_record: MidiKeyboardRecord = (
        keyboard_id,
        company_name.strip(),
        keys_number,
        price,
        has_pads.strip().lower() == "да",
    )

    MidiKeyboard.append(new_record)

    return new_record

def select_record(
    keyboard_id: int | None = None,
    company_name: str | None = None,
    keys_number: int | None = None,
    price: float | None = None,
    has_pads: str | None = None,
) -> list[MidiKeyboardRecord]:
    if (
        keyboard_id is None
        and company_name is None
        and keys_number is None
        and price is None
        and has_pads is None
    ):
        return MidiKeyboard.copy()

    has_pads_bool = None
    if has_pads is not None:
        has_pads_bool = has_pads.strip().lower() == "да"

    result: list[MidiKeyboardRecord] = []

    for record in MidiKeyboard:
        if keyboard_id is not None and record[0] != keyboard_id:
            continue

        if company_name is not None and record[1] != company_name:
            continue

        if keys_number is not None and record[2] != keys_number:
            continue

        if price is not None and record[3] != price:
            continue

        if has_pads_bool is not None and record[4] != has_pads_bool:
            continue

        result.append(record)

    return result
