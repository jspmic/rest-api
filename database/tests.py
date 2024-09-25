import unittest
import retrieve


class TestWorksheet(unittest.TestCase):
    def setUp(self):
        self.worksheet = retrieve.Worksheet

    def test_worksheet(self):
        with self.assertRaises(ValueError):
            self.worksheet("random_dir.xlsx")

    def test_stock_central(self):
        self.assertNotEqual(self.worksheet().stock_central(), [])

    def test_livraison_retour(self):
        self.assertNotEqual(self.worksheet().livraison_retour(), [])

    def test_input(self):
        self.assertNotEqual(self.worksheet().input(), [])

    def test_program(self):
        self.assertNotEqual(self.worksheet().program(), [])

    def test_districts(self):
        self.assertNotEqual(self.worksheet().districts(), [])

    def test_colline(self):
        self.assertNotEqual(self.worksheet().colline(), dict())


if __name__ == "__main__":
    unittest.main()
