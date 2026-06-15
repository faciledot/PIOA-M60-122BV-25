import unittest
from unittest.mock import patch

from src.db.tui import (
    _read_int,
    _read_float,
    _read_optional_int,
    _read_optional_float,
    _print_menu,
    _print_records,
    _add_keyboard,
    _show_all_keyboards,
    _find_keyboards_by_filter,
    run,
)


class TestPrintMenu(unittest.TestCase):
    @patch("builtins.print")
    def test_called(self, mock_print):
        _print_menu()
        self.assertTrue(mock_print.called)


class TestPrintRecords(unittest.TestCase):
    @patch("builtins.print")
    def test_empty(self, mock_print):
        _print_records([])
        mock_print.assert_called_with("Записи не найдены.")


class TestReadInt(unittest.TestCase):
    @patch("builtins.input", return_value="42")
    def test_valid(self, mock_input):
        self.assertEqual(_read_int(""), 42)


class TestReadFloat(unittest.TestCase):
    @patch("builtins.input", return_value="119.99")
    def test_valid(self, mock_input):
        self.assertEqual(_read_float(""), 119.99)


class TestReadOptionalInt(unittest.TestCase):
    @patch("builtins.input", return_value="42")
    def test_valid(self, mock_input):
        self.assertEqual(_read_optional_int(""), 42)

    @patch("builtins.input", return_value="")
    def test_empty(self, mock_input):
        self.assertIsNone(_read_optional_int(""))


class TestReadOptionalFloat(unittest.TestCase):
    @patch("builtins.input", return_value="119.99")
    def test_valid(self, mock_input):
        self.assertEqual(_read_optional_float(""), 119.99)

    @patch("builtins.input", return_value="")
    def test_empty(self, mock_input):
        self.assertIsNone(_read_optional_float(""))


class TestAddKeyboard(unittest.TestCase):
    def setUp(self):
        from src.db.backend.memory import MidiKeyboardDB
        import src.db.tui as tui_module
        tui_module.db = MidiKeyboardDB()

    @patch("builtins.input", side_effect=["1", "Akai", "25", "119.99", "да"])
    @patch("builtins.print")
    def test_success(self, mock_print, mock_input):
        _add_keyboard()
        printed = [str(c[0][0]) for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any("Запись добавлена" in p for p in printed))


class TestShowAllKeyboards(unittest.TestCase):
    def setUp(self):
        from src.db.backend.memory import MidiKeyboardDB
        import src.db.tui as tui_module
        tui_module.db = MidiKeyboardDB()

    @patch("builtins.print")
    def test_empty(self, mock_print):
        _show_all_keyboards()
        printed = [str(c[0][0]) for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any("Записи не найдены" in p for p in printed))


class TestFindKeyboardsByFilter(unittest.TestCase):
    def setUp(self):
        from src.db.backend.memory import MidiKeyboardDB
        import src.db.tui as tui_module
        tui_module.db = MidiKeyboardDB()
        tui_module.db.create(1, "Akai", 25, 119.99, "да")

    @patch("builtins.input", side_effect=["", "", "", "", ""])
    @patch("builtins.print")
    def test_no_filters(self, mock_print, mock_input):
        _find_keyboards_by_filter()
        printed = [str(c[0][0]) for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any("Akai" in p for p in printed))


class TestRun(unittest.TestCase):
    @patch("builtins.input", side_effect=["0"])
    @patch("builtins.print")
    def test_exit(self, mock_print, mock_input):
        run()
        printed = [str(c[0][0]) for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any("Выход из программы" in p for p in printed))

    @patch("builtins.input", side_effect=["5", "0"])
    @patch("builtins.print")
    def test_unknown_command(self, mock_print, mock_input):
        run()
        printed = [str(c[0][0]) for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any("Неизвестная команда" in p for p in printed))