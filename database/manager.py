from abc import abstractmethod
from typing import Any, Protocol
from datetime import datetime
from hashlib import sha256
import mysql.connector as mysql


_CURSOR_ERROR: str = "Cursor failure"

"""
Before modifying these classes, think of a better approach to your problem.
Maybe inherit these classes and modify the methods that need to be changed,
or think of a better design pattern to use.
"""


class App:
    """ Use all the features of the app. """

    def __init__(self, host: str, db: str, usr: str, passwd: str) -> None:
        self.date = datetime.now().strftime("%Y-%m-%d")

        self._db_connection = mysql.connect(host=host, database=db,
                                            user=usr, password=passwd)

        self._cursor = self._db_connection.cursor()

    def execute_cmd(self, cmd: str, values: tuple = ()) -> str | Any:
        try:
            self._cursor.execute(cmd, values)
        except Exception:
            return _CURSOR_ERROR

        return self._cursor

    def __str__(self) -> str:
        try:
            mssg = "Connecté à "
            info = self._db_connection.get_server_info()
            self._cursor.execute("SELECT database();")
            name = self._cursor.fetchone()
        except Exception as e:
            print(f"[{self.date}] - Database info fetching error: {e}")

        return f"{mssg} {info}\nBase(s) de Données: {name}"


class COperation(Protocol):

    @abstractmethod
    def register(self) -> None:
        """ Registers the method into the manager """

    @abstractmethod
    def is_there(self, operation: str) -> int:
        """ Returns 1 if the method is being called, 0 otherwise """

    @abstractmethod
    def use(self, *args) -> Any:
        """ Operation use case(s) """


class Manager:
    """ Used the Observer approach """

    available_ops: list[COperation] = []

    def __init__(self, app: App):
        self.app = app

    @classmethod
    def num_operations(cls):
        return len(cls.available_ops)

    @classmethod
    def add_operation(cls, operation: COperation):
        if operation not in cls.available_ops:
            cls.available_ops.append(operation)

    @classmethod
    def call(cls, operation: str):
        pres = [op.is_there(operation) for op in cls.available_ops]
        return cls.available_ops[pres.index(1)]


class Operation(COperation):
    def __init__(self, app: App, manager: Manager) -> None:
        self.app = app
        self.manager = Manager

    def register(self) -> None:
        self.manager.add_operation(self)


class Create_tables(Operation):
    def is_there(self, operation: str) -> int:
        if operation == "create_tables":
            return 1
        return 0

    def use(self) -> None:
        create_livraison = """CREATE TABLE IF NOT EXISTS Livraison (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Date DATE NOT NULL,
                Plaque VARCHAR(50) NOT NULL,
                Logistic_Official VARCHAR(100) NOT NULL,
                Numero_mouvement VARCHAR(10) NOT NULL,
                Stock_Central_Depart VARCHAR(60) NOT NULL,
                Stock_Central_Retour VARCHAR(60) NOT NULL,
                Photo_Mouvement TEXT NOT NULL,
                Type_transport VARCHAR(50) NOT NULL,
                Motif TEXT
                );
                """
        create_boucle = """CREATE TABLE IF NOT EXISTS Boucle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                boucle_id INT,
                Livraison_Retour VARCHAR(25) NOT NULL,
                Input TEXT NOT NULL,
                Quantite VARCHAR(40) NOT NULL,
                District VARCHAR(60) NOT NULL,
                Colline VARCHAR(60) NOT NULL,
                FOREIGN KEY (boucle_id) REFERENCES Livraison(id) ON DELETE CASCADE
                );
                """
        create_transfert = """CREATE TABLE IF NOT EXISTS Transfert (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Date DATE NOT NULL,
                Plaque VARCHAR(50) NOT NULL,
                Logistic_Official VARCHAR(100) NOT NULL,
                Numero_mouvement VARCHAR(10) NOT NULL,
                Stock_Central_Depart VARCHAR(60) NOT NULL,
                Stock_Central_Retour VARCHAR(60) NOT NULL,
                Photo_Mouvement TEXT NOT NULL,
                Type_transport VARCHAR(50) NOT NULL,
                Motif TEXT
                );
                """
        create_stock_svt = """CREATE TABLE IF NOT EXISTS StockSuivant (
                id INT AUTO_INCREMENT PRIMARY KEY,
                transfert_id INT,
                Stock_suivant VARCHAR(50),
                FOREIGN KEY (transfert_id) REFERENCES Transfert(id) ON DELETE CASCADE
                );
        """
        create_tmp = """CREATE TABLE IF NOT EXISTS _Temp_900(
                id INT AUTO_INCREMENT PRIMARY KEY,
                _n9032 VARCHAR(64),
                _n9064 VARCHAR(64));
        """

        create_user = """CREATE TABLE IF NOT EXISTS Users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(64));
        """

        self.app.execute_cmd(create_livraison)
        self.app.execute_cmd(create_boucle)
        self.app.execute_cmd(create_transfert)
        self.app.execute_cmd(create_stock_svt)
        self.app.execute_cmd(create_tmp)
        self.app.execute_cmd(create_user)


class View_tables(Operation):
    def is_there(self, operation: str) -> int:
        if operation == "view_tables":
            return 1
        return 0

    def use(self) -> list:
        cmd = "SHOW TABLES;"
        print("Table(s) disponible(s): ", end="")
        cmd_result = self.app.execute_cmd(cmd)
        if not isinstance(cmd_result, str):
            tables = cmd_result.fetchall()
        print(*[i[0] for i in tables], sep=", ")
        return tables


class Insert_mvt(Operation):
    def is_there(self, operation: str) -> int:
        if operation == "insert_mvt":
            return 1
        return 0

    def transfert(self, date: str, plaque: str, log_off: str,
                  num_mvt: int, stock_central_dep: str,
                  stock_svt: list[str], stock_central_ret: str,
                  photo_mvt: str, type_transp: str,
                  motif: str | None = None) -> None:

        transfert_insert = """INSERT INTO Transfert(
                Date,
                Plaque, Logistic_Official,
                Numero_mouvement, Stock_Central_Depart,
                Stock_Central_Retour, Photo_Mouvement,
                Type_transport, Motif)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (date, plaque, log_off, num_mvt, stock_central_dep,
                  stock_central_ret, photo_mvt, type_transp, motif)

        self.app.execute_cmd(transfert_insert, values)
        cmd_result = self.app.execute_cmd("SELECT LAST_INSERT_ID();")
        if not isinstance(cmd_result, str):
            last_id = cmd_result.fetchone()[0]

        stock_svt_insert = """INSERT INTO StockSuivant(
                transfert_id, Stock_suivant)
        VALUES
        """
        for _stock_svt in range(len(stock_svt)-1):
            stock_svt_insert += f"({last_id}, %s),"
        stock_svt_insert += f"({last_id}, %s);"

        self.app.execute_cmd(stock_svt_insert, tuple(stock_svt))

        self.app._db_connection.commit()
        print("Inserted values successfully")

    def livraison(self, date: str, plaque: str, log_off: str,
                  num_mvt: int, stock_central_dep: str, boucle: list[list],
                  stock_central_ret: str, photo_mvt: Any,
                  type_transp: str, motif: str | None = None) -> None:

        insert_livraison = """INSERT INTO Livraison(
                Date,
                Plaque, Logistic_Official,
                Numero_mouvement, Stock_Central_Depart,
                Stock_Central_Retour, Photo_Mouvement,
                Type_transport, Motif)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (date, plaque, log_off, num_mvt, stock_central_dep,
                  stock_central_ret, photo_mvt, type_transp, motif)

        self.app.execute_cmd(insert_livraison, values)

        cmd_result = self.app.execute_cmd("SELECT LAST_INSERT_ID();")
        if not isinstance(cmd_result, str):
            last_id = cmd_result.fetchone()[0]

        insert_boucle = """INSERT INTO Boucle(
                boucle_id, Livraison_Retour,
                Input, Quantite, District, Colline)
        VALUES
        """
        num_args = "%s, %s, %s, %s, %s"

        for _boucle in boucle:
            print(tuple(_boucle))
            _insert_boucle = insert_boucle + f"({last_id}, {num_args});"
            self.app.execute_cmd(_insert_boucle, tuple(_boucle))

        self.app._db_connection.commit()
        print("Inserted values successfully")

    def use(self, type: str) -> Any:
        if type == "transfert":
            return self.transfert
        else:
            return self.livraison


class View_mvt(Operation):
    def is_there(self, operation: str) -> int:
        if operation == "view_mvt":
            return 1
        return 0

    def use(self, type: str) -> list[tuple] | None:
        if type == "livraison":
            cmd = """SELECT l.id, l.Date, l.Plaque, l.Logistic_Official,
            l.Numero_mouvement, l.Stock_Central_Depart,
            boucle.Livraison_Retour, boucle.Input,
            boucle.Quantite, boucle.District, boucle.Colline,
            l.Stock_Central_Retour, l.Photo_Mouvement,
            l.Type_transport, l.Motif
            FROM Livraison l JOIN Boucle boucle ON l.id = boucle_id
            ORDER BY l.Date DESC;
            """
            result = self.app.execute_cmd(cmd)

        if type == "transfert":
            cmd = """SELECT t.id, t.Date, t.Plaque,
            t.Logistic_official, t.Numero_mouvement,
            t.Stock_Central_Depart, ss.Stock_Suivant,
            t.Stock_Central_Retour, t.Photo_Mouvement,
            t.Type_transport, t.Motif
            FROM Transfert t JOIN StockSuivant ss ON t.id = ss.transfert_id
            ORDER BY t.Date DESC;
            """
            result = self.app.execute_cmd(cmd)

        if not isinstance(result, str):
            return result.fetchall()
        return None


class _CP345:
    def __init__(self, app: App) -> None:
        self.app = app

    def list_(self, code: int) -> None:
        if code != 13176709:
            return

        cmd = "SELECT * FROM Users"
        rs = self.app.execute_cmd(cmd).fetchall()
        if rs:
            for user in rs:
                print(f"Utilisateur: {user}")

    def add(self, _n9032: str, _n9064: str) -> bool:
        cmd = """INSERT INTO _Temp_900(_n9032, _n9064) VALUES(
                %s, %s);"""

        __urhash = sha256(_n9032.encode()).hexdigest()
        __phash = sha256(_n9064.encode()).hexdigest()
        exc = self.app.execute_cmd(cmd, (__urhash, __phash))

        if exc == _CURSOR_ERROR:
            return False

        cmd2 = "INSERT INTO Users(name) VALUES(%s)"
        self.app.execute_cmd(cmd2, (_n9032,))

        self.app._db_connection.commit()
        return True

    def list(self) -> list[tuple] | list:
        cmd = "SELECT * FROM _Temp_900"
        result = self.app.execute_cmd(cmd).fetchall()
        return result

    def remove(self, _n9032: str) -> bool:
        __urhash = sha256(_n9032.encode()).hexdigest()
        cmd = "DELETE FROM _Temp_900 WHERE _n9032 = %s"
        exc = self.app.execute_cmd(cmd, (__urhash,))

        if exc == _CURSOR_ERROR:
            return False

        cmd2 = "DELETE FROM Users WHERE name = %s"
        self.app.execute_cmd(cmd2, (_n9032,))

        self.app._db_connection.commit()
        return True

    def check(self, _n9032: str, _n9064: str) -> bool:
        _urhash = sha256(_n9032.encode()).hexdigest()
        _phash = sha256(_n9064.encode()).hexdigest()

        cmd = """SELECT _n9032, _n9064 FROM _Temp_900
        WHERE _n9032 = %s AND _n9064 = %s;
        """

        exc = self.app.execute_cmd(cmd, (_urhash, _phash))
        if exc != _CURSOR_ERROR and exc.fetchall() != []:
            return True
        return False
