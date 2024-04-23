import os
from typing import Tuple

import psycopg2
from dotenv import load_dotenv
from flask import Flask, abort, g, render_template

from admin.admin import admin
from DataBase import DataBase


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True


app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(admin, url_prefix="/admin")
app.secret_key = SECRET_KEY


menu = [
    {"name": "Главная страница", "url": "/"},
    {"name": "Список исполнителей", "url": "/contractors"},
    {"name": "Список заказчиков", "url": "/customers"},
]


def connect_db():
    """
    Функция для установления соединения с БД
    """
    conn = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    return conn


def create_db() -> None:
    """
    Функция для создания таблиц в БД
    """
    db = connect_db()
    with app.open_resource("postgres_db.sql", mode="r") as f:
        db.cursor().execute(f.read())
    db.commit()
    db.close()


def get_db():
    """
    Функция соединения с БД, если оно еще не установлено
    """
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request() -> None:
    """
    Функция для установления соединения с БД перед выполнением запроса
    """
    global dbase
    db = get_db()
    dbase = DataBase(db)


@app.route("/")
def main_page() -> str:
    """
    Представление для отображения главной страницы
    """
    return render_template("main_page.html", title="Сайт для заказов", menu=menu)


@app.route("/contractors")
def contractor_list() -> str:
    """
    Представление для отображения списка исполнителей
    """
    return render_template(
        "contractor_list.html",
        title="Список исполнителей",
        menu=menu,
        contractors=dbase.getContractorsList(),
    )


@app.route("/customers")
def customer_list() -> str:
    """
    Представление для отображения списка заказчиков
    """
    return render_template(
        "customer_list.html",
        title="Список заказчиков",
        menu=menu,
        customers=dbase.getCustomersList(),
    )


@app.route("/contractor/<alias>")
def showContractor(alias: str) -> str:
    """
    Представление для отображения детальной страницы исполнителя
    """
    contractor_user = dbase.getContractor(alias)
    if not contractor_user:
        abort(404)
    return render_template("contractor.html", menu=menu, contractor=contractor_user)


@app.route("/customer/<alias>")
def showCustomer(alias: str) -> str:
    """
    Представление для отображения детальной страницы заказчика
    """
    customer_user = dbase.getCustomer(alias)
    if not customer_user:
        abort(404)
    return render_template("customer.html", menu=menu, customer=customer_user)


@app.teardown_appcontext
def close_db(error) -> None:
    """
    Функция для закрытия соединение с БД, если оно было установлено
    """
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.errorhandler(404)
def pageNotFound(error) -> Tuple[str, int]:
    """
    Функция для отображения страницы при ошибке 404 (отсутсвие страницы по адресу)
    """
    return render_template("page404.html", title="Страница не найдена", menu=menu), 404


if __name__ == "__main__":
    create_db()
    app.run(debug=True)
