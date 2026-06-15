from .errors import (
    DuplicateIDError,
    EmptyCompanyNameError,
    InvalidHasPadsError,
    InvalidKeysNumberError,
    InvalidPriceError,
)

type MidiKeyboardRecord = tuple[int, str, int, float, bool]


class MidiKeyboardDB:
    def __init__(self) -> None:
        self._records: list[MidiKeyboardRecord] = []

    def create(
        self,
        keyboard_id: int,
        company_name: str,
        keys_number: int,
        price: float,
        has_pads: str,
    ) -> MidiKeyboardRecord:

        if not company_name or not company_name.strip():
            raise EmptyCompanyNameError("Название компании не может быть пустым.")

        if keys_number <= 0:
            raise InvalidKeysNumberError("Поле keys_number не может быть отрицательным или нулевым.")
        if keys_number > 88:
            raise InvalidKeysNumberError("Количество клавиш не может превышать 88.")

        if price < 0:
            raise InvalidPriceError("Поле price не может быть отрицательным.")

        has_pads_value = has_pads.strip().lower()
        if has_pads_value not in ("да", "нет"):
            raise InvalidHasPadsError("Поле has_pads должно принимать значения 'да' или 'нет'.")

        if any(record[0] == keyboard_id for record in self._records):
            raise DuplicateIDError(f"Запись с id={keyboard_id} уже существует.")

        new_record: MidiKeyboardRecord = (
            keyboard_id,
            company_name.strip(),
            keys_number,
            price,
            has_pads_value == "да",
        )
        self._records.append(new_record)
        return new_record

    def select(
        self,
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
            return self._records.copy()

        has_pads_bool = None
        if has_pads is not None:
            has_pads_value = has_pads.strip().lower()
            if has_pads_value not in ("да", "нет"):
                raise InvalidHasPadsError("Поле has_pads должно принимать значения 'да' или 'нет'.")
            has_pads_bool = has_pads_value == "да"

        result: list[MidiKeyboardRecord] = []

        for record in self._records:
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