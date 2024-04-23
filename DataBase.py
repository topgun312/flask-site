from typing import Any

from psycopg2.extras import NamedTupleCursor


class DataBase:
    """
    Класс для взаимодействия представлений с базой данных
    """

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor(cursor_factory=NamedTupleCursor)

    def getContractorsList(self) -> Any:
        """
        Функция для получения списка исполнителей из БД
        """
        try:
            self.__cur.execute(
                "SELECT con.conname, con.email, con.phone, con.experience, con.url, cus.cusname FROM contractors con LEFT JOIN customers cus ON con.id = cus.id ORDER BY cus.id"
            )
            result = self.__cur.fetchall()
            if result:
                return result
        except Exception as ex:
            print("Ошибка получения данных из БД", str(ex))

    def getCustomersList(self) -> Any:
        """
        Функция для получения списка заказчиков из БД
        """
        try:
            self.__cur.execute(
                "SELECT cus.cusname, cus.email, cus.phone, cus.url, con.conname FROM customers cus LEFT JOIN contractors con ON cus.id = con.id ORDER BY cus.id"
            )
            result = self.__cur.fetchall()
            if result:
                return result
        except Exception as ex:
            print("Ошибка получения данных из БД", str(ex))

    def getContractor(self, alias: str) -> Any:
        """
        Функция для получения информации об исполнителе из БД
        """
        try:
            self.__cur.execute(
                f"SELECT con.conname, con.email, con.phone, con.experience, con.url, cus.cusname, cus.contractor_id FROM contractors con LEFT JOIN customers cus ON con.id = cus.contractor_id WHERE con.url LIKE '{alias}' LIMIT 1"
            )
            result = self.__cur.fetchone()
            if result:
                return result
        except Exception as ex:
            print("Ошибка получения данных из БД", str(ex))

    def getCustomer(self, alias: str) -> Any:
        """
        Функция для получения информации об заказчике из БД
        """
        try:
            self.__cur.execute(
                f"SELECT cus.cusname, cus.email, cus.phone, cus.contractor_id, cus.url, con.conname, con.id FROM customers cus LEFT JOIN contractors con ON cus.contractor_id = con.id WHERE cus.url LIKE '{alias}' LIMIT 1"
            )
            result = self.__cur.fetchone()
            if result:
                return result
        except Exception as ex:
            print("Ошибка получения данных из БД", str(ex))
