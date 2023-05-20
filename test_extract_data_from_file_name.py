# test_mi_modulo.py
import unittest
from extract_date_from_file_utils import extractDateTimeFromFileName
from datetime import date, datetime

class TestExtractDataFromFileName(unittest.TestCase):

    def test_extraerfecha(self):
        self.assertEqual(extractDateTimeFromFileName("2020-01-01"), datetime(2020, 1, 1, 0, 0, 0))
        self.assertEqual(extractDateTimeFromFileName("2020-01-01_01-01-00"), datetime(2020, 1, 1, 1, 1, 0))


if __name__ == "__main__":
    unittest.main()