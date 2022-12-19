from flask import Flask, render_template, request, flash, redirect, url_for, session
from db_connect import connect_to_db, choose_model
import psycopg2.extras
import psycopg2
import re

app = Flask(__name__)
app.secret_key = 'skshop'

@app.route('/')
def home_page():
    context = {'page_title': 'SK shop'}
    return render_template("main_page.html", **context)


@app.route('/shoes')
def all_catalog():
    return 'Catalog'


@app.route('/<int:product_articul>')
def product_card(product_articul):
    product = choose_model(product_articul)
    context = {
        'title': product['product_title'],
        'page_title': product['product_title'],
        'articul': product['product_articul'],
        'sizes': product['product_sizes'].split(),
        'description': product['product_description'],
        'price': product['product_price']
    }
    if product != None:
        return render_template("product_card.html", **context)

    return render_template("error.html", error="Такого продукта не существует")


@app.route('/personal-area')
def personal_area():
    context = {'page_title': 'Личный кабинет'}
    return render_template("personal_area.html", **context)


@app.route('/order')
def order_list():
    return 'Корзина'


@app.route('/orders')
def orders():
    context = {'page_title': 'Заказы'}
    return render_template("orders.html", **context)


@app.route('/favorites')
def favorites():
    context = {'page_title': 'Избранное'}
    return render_template("favorites.html", **context)


@app.route('/registration', methods=["POST", "GET"])
def registration():
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'name' in request.form and 'surname' in request.form and 'gender' in request.form \
            and 'email' in request.form and 'number' in request.form and 'password' in request.form and 'repeat-password' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        gender = request.form['gender']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']
        repeat_rassword = request.form['repeat-password']

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('Аккаунт уже существует!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Неправильно введен email адрес')
        elif not number or 11 != len(number):
            flash('Неправильно введет номер телефона')
        elif not password or len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов')
        elif password != repeat_rassword:
            flash('Пароли не совпадают')
        elif not name or not surname or not gender:
            flash('Пожалуйста, заполните форму полностью')
        else:
            cursor.execute(
                "INSERT INTO users (id, user_name, surname, gender, email, phone_number, password) VALUES (default, %s,%s,%s,%s,%s,%s)",
                (name, surname, gender, email, number, password))
            conn.commit()
            flash('Регистрация прошла успешно')
    elif request.method == 'POST':
        flash('Пожалуйста, заполните форму')

    context = {'page_title': 'Регистрация'}
    return render_template("registration.html", **context)


@app.route('/login', methods=["POST", "GET"])
def login():
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT email, password FROM users')
        accounts = cursor.fetchall()

        for acc in accounts:
            if acc['email'] == email and acc['password'] == password:
                flash('Вы вошли в аккаунт')
                redirect(url_for('personal_area'))
            elif acc['email'] != email and acc['password'] == password:
                flash('Неправильный email')
            elif acc['email'] == email and acc['password'] != password:
                flash('Неправильный пароль')
            else:
                flash('Такого аккаунта не существует')
    context = {'page_title': 'Вход'}
    return render_template("login.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
