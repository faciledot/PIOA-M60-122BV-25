import unittest

from src.db.backend.errors import (
    DuplicateIDError,
    EmptyCompanyNameError,
    InvalidHasPadsError,
    InvalidKeysNumberError,
    InvalidPriceError,
)
from src.db.backend.memory import MidiKeyboardDB


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.db = MidiKeyboardDB()
        self.assertIsInstance(self.db, MidiKeyboardDB)

    def test_create_record(self):
        cases = [
            (1, "Akai", 25, 119.99, "да"),
            (2, "Arturia", 49, 299.99, "нет"),
        ]

        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.db.create(*test_data)
                expected = (*test_data[:4], test_data[4] == "да")
                self.assertEqual(record, expected)

    def test_create_record_empty_company_name(self):
        with self.assertRaises(EmptyCompanyNameError):
            self.db.create(1, "", 25, 119.99, "да")

    def test_create_record_invalid_keys_number(self):
        with self.assertRaises(InvalidKeysNumberError):
            self.db.create(1, "Akai", 0, 119.99, "да")

    def test_create_record_negative_price(self):
        with self.assertRaises(InvalidPriceError):
            self.db.create(1, "Akai", 25, -10.0, "да")

    def test_create_record_invalid_has_pads(self):
        with self.assertRaises(InvalidHasPadsError):
            self.db.create(1, "Akai", 25, 119.99, "maybe")

    def test_create_record_duplicate_id(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        with self.assertRaises(DuplicateIDError):
            self.db.create(1, "Roland", 88, 999.99, "нет")

    def test_select_all(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        records = self.db.select()
        self.assertEqual(len(records), 1)

    def test_select_by_id(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        self.db.create(2, "Arturia", 49, 299.99, "нет")
        records = self.db.select(keyboard_id=2)
        self.assertEqual(len(records), 1)

    def test_select_by_company_name(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        self.db.create(2, "Akai", 49, 249.99, "да")
        records = self.db.select(company_name="Akai")
        self.assertEqual(len(records), 2)

    def test_select_by_has_pads(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        self.db.create(2, "Arturia", 49, 299.99, "нет")
        records = self.db.select(has_pads="да")
        self.assertEqual(len(records), 1)

    def test_select_combined_filters(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        self.db.create(2, "Arturia", 49, 299.99, "нет")
        self.db.create(3, "Akai", 49, 249.99, "да")
        records = self.db.select(company_name="Akai", has_pads="да")
        self.assertEqual(len(records), 2)