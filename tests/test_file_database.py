import os
import tempfile
import unittest

from src.db.backend.file import FileMidiKeyboardDB
from src.db.backend.errors import InvalidJSONError


class TestFileDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_keyboards.json")
        self.db = FileMidiKeyboardDB(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_create_record(self):
        record = self.db.create(1, "Akai", 25, 119.99, "да")
        self.assertEqual(record, (1, "Akai", 25, 119.99, True))

    def test_data_persists(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        db2 = FileMidiKeyboardDB(self.test_file)
        records = db2.select()
        self.assertEqual(len(records), 1)

    def test_select_by_id(self):
        self.db.create(1, "Akai", 25, 119.99, "да")
        self.db.create(2, "Arturia", 49, 299.99, "нет")
        records = self.db.select(keyboard_id=2)
        self.assertEqual(len(records), 1)

    def test_invalid_json(self):
        with open(self.test_file, "w") as f:
            f.write("not json")
        with self.assertRaises(InvalidJSONError):
            FileMidiKeyboardDB(self.test_file)