# src/db/backend/errors.py

class MidiKeyboardTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей MidiKeyboard."""
    pass


class InvalidKeysNumberError(MidiKeyboardTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным количеством клавиш."""
    pass


class InvalidPriceError(MidiKeyboardTableError):
    """Ошибка, возникающая при попытке создать запись с некорректной ценой."""
    pass


class InvalidHasPadsError(MidiKeyboardTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным значением поля has_pads."""
    pass


class EmptyCompanyNameError(MidiKeyboardTableError):
    """Ошибка, возникающая при попытке создать запись с пустым названием компании."""
    pass


class DuplicateIDError(MidiKeyboardTableError):
    """Ошибка, возникающая при попытке создать запись с уже существующим идентификатором."""
    pass