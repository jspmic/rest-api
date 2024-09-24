import unittest
import manager
import retrieve
import mysql.connector as mysql


DB_ERRORS = mysql.errors


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = manager.App

    def test_connection(self):
        with self.assertRaises(DB_ERRORS.DatabaseError):
            # If invalid values are provided to the connector
            self.app("", "", "", "")

    def test_cursor(self):
        self.assertEqual(self.app.execute_cmd(self, ""), manager._CURSOR_ERROR)


class TestManager(unittest.TestCase):
    def setUp(self):
        self._manager = manager
        self.manager = manager.Manager

    def test_num_operations(self):
        self._manager.Insert_mvt(self._manager.App,
                                 self._manager.Manager).register()

        self._manager.View_mvt(self._manager.App,
                               self._manager.Manager).register()

        self._manager.Create_tables(self._manager.App,
                                    self._manager.Manager).register()

        self._manager.View_tables(self._manager.App,
                                  self._manager.Manager).register()

        self.assertEqual(self.manager.num_operations(), 4)


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
