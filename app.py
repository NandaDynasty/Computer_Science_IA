import pdfkit
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, session
from flask_cors import CORS
import mysql.connector
from sqlalchemy import create_engine, select, and_, delete
from sqlalchemy import text
import datetime
from datetime import datetime as dt
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, joinedload
from notifications import email_inventory, email_order_details, email_order_admin, email_stock, \
    preparation_notification, dispatch_notification
from adminvalidate import validateadmincredentials
from newproduct import createitem
from validatelogin import validatecredentials
import secrets
import json
from processorders import process_orders
from engine import engine
from models.customersmodels import customersmodel, customers, updatedcustomer
from models.ordersmodels import orders, order_status
from models.productmodels import products
from models.revenuemodels import monthlyrevenue, mrmodel
from models.stockmodels import stock, stockmodel
from models.orderpricemodels import orderprice
from models.cakerevenuemodel import cakerevenue, crmodel
from models.breadrevenuemodel import breadrevenue, brmodel
from models.morerevenuemodel import morerevenue, moremodel
from models.savouryrevenuemodel import savouryrevenue, srmodel
from models.prodstockmodels import prodstock, productstockmodel

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if validatecredentials(email, password):
            session['user'] = {'email': email}
            return redirect(url_for('order'))
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render_template('Log-in.html', error_message=error_message)
    return render_template('Log-in.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        address = request.form.get('address')
        email = request.form.get('email')
        number = request.form.get('phone-number')
        pword = request.form.get('password')
        hashed_password = generate_password_hash(pword, method="sha256")
        with engine.connect() as connection:
            stmt = select(customers).where(customers.email == email)
            result = connection.execute(stmt)
            if not result.fetchone():
                customer_obj = customersmodel(first_name, last_name, address, number, email, hashed_password)
                customer_obj.insert()
        session['user'] = {'email': email}
        return redirect(url_for('order'))
    return render_template('signup.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        cart_data = request.get_json()
        user_email = user.get('email')
        process_orders(cart_data, user_email)
        email_order_details(user_email, cart_data)
        email_order_admin(cart_data)
        return jsonify({"success": True})
    return render_template('orderpage.html')

@app.route('/order_success')
def order_success():
    return render_template('order_success.html')

@app.route('/profile', methods=['POST', 'GET'])
def account():
    user = session.get('user')
    if user:
        with engine.connect() as connection:
            stmt = select(customers.first_name, customers.last_name, customers.phone_number, customers.address,
                          customers.password).where(customers.email == user['email'])
            result = connection.execute(stmt).fetchone()

        if request.method == 'POST':
            first_name = request.form.get('firstname')
            last_name = request.form.get('lastname')
            email = request.form.get('email')
            user['email'] = email
            number = request.form.get('number')
            address = request.form.get('address')
            password = request.form.get('password')
            hashed_password = generate_password_hash(password, method="sha256")
            customer_obj = updatedcustomer(email, first_name, last_name, address, number, email, hashed_password)
            customer_obj.update()
            return redirect(url_for('order'))

        fname = result.first_name
        lname = result.last_name
        number = result.phone_number
        address = result.address
        pword = result.password

        return render_template('profilepage.html', fname=fname, lname=lname, email=user['email'], phoneno=number,
                               address=address, pword=pword)

    return redirect(url_for('login'))

@app.route('/myorders')
def myorders():
    return render_template('myorders.html')

@app.route('/get_user_orders_data', methods=['GET'])
def get_user_orders_data():
    user = session.get('user')
    useremail = user['email']
    with engine.connect() as connection:
        stmt = select(customers.customer_id).where(customers.email == useremail)
        id = connection.execute(stmt).fetchone()
        Session = sessionmaker(bind=engine)
        conn = Session()
        query = conn.query(orders, products, customers).join(products).join(customers)
        result = query.options(joinedload(orders.products), joinedload(orders.customers)).all()
        orders_data = []
        for order, product, customer in result:
            order_data = {
                "order_id": order.order_id,
                "product_name": product.product_name,
                "quantity": order.quantity,
                "order_customer": order.customer_id,
                "date_of_order": order.date.strftime("%Y-%m-%d"),
                "status": order.status
            }
            if order_data["order_customer"] == id[0]:
                orders_data.append(order_data)

        return jsonify(orders_data)


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if validateadmincredentials(email, password):
            session['user'] = {'email': email}
            return redirect(url_for('admin'))
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render_template('adminlogin.html', error_message=error_message)
    return render_template('adminlogin.html')

@app.route('/admin')
def admin():
    return render_template("adminpage.html")


@app.route('/newitem', methods=['POST'])
def create_item():
    if request.method == 'POST':
        product = request.form.get('product_name')
        type = request.form.get('product_type')
        price = request.form.get('price')
        image = request.files['product_image']
        details = request.form.get('product_details')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            createitem(product, type, filename, price, details)
            return redirect(url_for('admin'))

@app.route('/deleteitem', methods=['GET', 'POST'])
def delete_item():
    if request.method == 'POST':
        product = request.form.get('product_name')
        with engine.connect() as connection:
            stmt = delete(products).where(products.product_name == product)
            connection.execute(stmt)
            connection.commit()
        return redirect(url_for('admin'))
    return render_template('DeleteItem.html')

ext = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext

@app.route('/newitem', methods=['GET'])
def show_new_item_form():
    return render_template("NewItem.html")


@app.route('/menu', methods=['GET'])
def get_menu():
    with engine.connect() as connection:
        try:
            stmt = select(products.product_name, products.product_type, products.product_image, products.price, products.product_details)
            result = connection.execute(stmt)
            menu_data = result.fetchall()
            menu = [{
                "name": row.product_name,
                "type": row.product_type,
                "imageLink": url_for('uploaded_file', filename=row.product_image),
                "price": row.price,
                "details": row.product_details,
                "stock": connection.execute(select(prodstock.current_stock).where(prodstock.product_name == row.product_name)).fetchone().current_stock
                if row.product_type != "Cake"
                else None
            } for row in menu_data]
            return jsonify(menu)
        except SQLAlchemyError as e:
            print(f"SQLAlchemy error: {e}")
            return jsonify(error=str(e)), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/monthlyrevenue')
def revenue():
    date = datetime.date.today()
    month = date.strftime("%B")
    year = date.strftime("%Y")
    with engine.connect() as connection:
        stmt = select(monthlyrevenue.total_revenue).where(and_(monthlyrevenue.year == year, monthlyrevenue.month == month))
        result = connection.execute(stmt).fetchone()
        if result:
            rev = result[0]
        else:
            rev = 0
        stmt = select(cakerevenue.revenue).where(and_(cakerevenue.year == year, cakerevenue.month == month))
        result = connection.execute(stmt).fetchone()
        if result:
            crev = result[0]
        else:
            crev = 0
        stmt = select(breadrevenue.revenue).where(and_(breadrevenue.year == year, breadrevenue.month == month))
        result = connection.execute(stmt).fetchone()
        if result:
            brev = result[0]
        else:
            brev = 0
        stmt = select(morerevenue.revenue).where(and_(morerevenue.year == year, morerevenue.month == month))
        result = connection.execute(stmt).fetchone()
        if result:
            mrev = result[0]
        else:
            mrev = 0
        stmt = select(savouryrevenue.revenue).where(and_(savouryrevenue.year == year, savouryrevenue.month == month))
        result = connection.execute(stmt).fetchone()
        if result:
            srev = result[0]
        else:
            srev = 0
    return render_template("monthlyrevenue.html", revenue=rev, breads_revenue=brev, cakes_revenue=crev, more_items_revenue=mrev, savoury_items_revenue=srev)

@app.route('/update_revenue', methods=['POST','GET'])
def update_revenue():
    if request.method == 'POST':
        month = request.form.get('month_choice')
        year = request.form.get('year_choice')
        with engine.connect() as connection:
            stmt = select(monthlyrevenue.total_revenue).where(
                and_(monthlyrevenue.year == year, monthlyrevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                rev = result[0]
            else:
                rev = 0
            stmt = select(cakerevenue.revenue).where(and_(cakerevenue.year == year, cakerevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                crev = result[0]
            else:
                crev = 0
            stmt = select(breadrevenue.revenue).where(and_(breadrevenue.year == year, breadrevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                brev = result[0]
            else:
                brev = 0
            stmt = select(morerevenue.revenue).where(and_(morerevenue.year == year, morerevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                mrev = result[0]
            else:
                mrev = 0
            stmt = select(savouryrevenue.revenue).where(and_(savouryrevenue.year == year, savouryrevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                srev = result[0]
            else:
                srev = 0
        return render_template("monthlyrevenue.html", revenue=rev, breads_revenue=brev, cakes_revenue=crev,
                               more_items_revenue=mrev, savoury_items_revenue=srev)

@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        date = datetime.date.today()
        month = date.strftime("%B")
        year = date.strftime("%Y")
        with engine.connect() as connection:
            stmt = select(monthlyrevenue.total_revenue).where(
                and_(monthlyrevenue.year == year, monthlyrevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                rev = result[0]
            else:
                rev = 0
            stmt = select(cakerevenue.revenue).where(and_(cakerevenue.year == year, cakerevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                crev = result[0]
            else:
                crev = 0
            stmt = select(breadrevenue.revenue).where(and_(breadrevenue.year == year, breadrevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                brev = result[0]
            else:
                brev = 0
            stmt = select(morerevenue.revenue).where(and_(morerevenue.year == year, morerevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                mrev = result[0]
            else:
                mrev = 0
            stmt = select(savouryrevenue.revenue).where(
                and_(savouryrevenue.year == year, savouryrevenue.month == month))
            result = connection.execute(stmt).fetchone()
            if result:
                srev = result[0]
            else:
                srev = 0

        date = dt.now()
        formatted_date = date.strftime("%Y-%m-%d")

        time = dt.now()
        formatted_time = time.strftime("%H:%M:%S")

        data = {
            'revenue': rev,
            'breads_revenue': brev,
            'cake_revenue': crev,
            'more_revenue': mrev,
            'savoury_revenue': srev,
            'date': formatted_date,
            'time': formatted_time
        }


        # Render the HTML template with the data
        rendered_html = render_template('monthlyrevenuepdf.html', **data)

        # Convert the rendered HTML to PDF
        pdfkit.from_string(rendered_html, 'static/monthly_revenue_report.pdf', configuration=pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"))
        return 'PDF export complete. <a href="/static/monthly_revenue_report.pdf" download>Download PDF</a>'

@app.route('/adminorders')
def adminorders():
    return render_template("adminorders.html")

@app.route('/get_orders_data', methods=['GET'])
def get_orders_data():
    with engine.connect() as connection:
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            query = session.query(orders, products, customers).join(products).join(customers)
            result = query.options(joinedload(orders.products), joinedload(orders.customers)).all()
            orders_data = []
            for order, product, customer in result:
                order_data = {
                    "order_id": order.order_id,
                    "product_name": product.product_name,
                    "quantity": order.quantity,
                    "customer_first_name": customer.first_name,
                    "customer_last_name": customer.last_name,
                    "delivery_address": customer.address,
                    "date_of_order": order.date.strftime("%Y-%m-%d"),
                    "status": order.status
                }
                if order_data["status"] == "Pending":
                    orders_data.append(order_data)

            return jsonify(orders_data)
        except SQLAlchemyError as e:
            print(f"SQLAlchemy error: {e}")
            return jsonify(error=str(e)), 500


@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    try:
        order = order_status(order_id)
        order.update()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/prepare_order/<int:order_id>', methods=['POST'])
def prepare_order(order_id):
    try:
        with engine.connect() as connection:
            stmt = select(orders.customer_id).where(orders.order_id == order_id)
            customerid = connection.execute(stmt).fetchone()
            customerid = customerid[0]
            stmt = select(customers.email).where(customers.customer_id == customerid)
            email = connection.execute(stmt).fetchone()
            email = email[0]
            preparation_notification(email)
            return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/dispatch_order/<int:order_id>', methods=['POST'])
def dispatch_order(order_id):
    try:
        with engine.connect() as connection:
            stmt = select(orders.customer_id).where(orders.order_id == order_id)
            customerid = connection.execute(stmt).fetchone()
            customerid = customerid[0]
            stmt = select(customers.email).where(customers.customer_id == customerid)
            email = connection.execute(stmt).fetchone()
            email = email[0]
            dispatch_notification(email)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/stock')
def stockpage():
    return render_template("stockchoicepage.html")

@app.route('/inventory')
def inventory():
    with engine.connect() as connection:
        stmt = select(stock)
        result = connection.execute(stmt)
        inventory_data = [
            {
                "ingredient_name": row.ingredient_name,
                "current_stock": row.current_stock,
                "minimum_stock": row.minimum_stock,
                "price": row.price
            }
            for row in result
        ]
        return render_template("inventory.html", inventory_data=inventory_data)

@app.route('/addingredient', methods=['GET','POST'])
def add_ingredient():
    if request.method == 'POST':
        ing_name = request.form.get("ingredient_name")
        current_quantity = request.form.get("current_quantity")
        reorder_quantity = request.form.get("reorder_quantity")
        price = request.form.get("ingredient_price")
        stock_obj = stockmodel(ing_name, current_quantity, reorder_quantity, price)
        stock_obj.insert()
        return redirect(url_for('add_ingredient'))
    return render_template("addingredient.html")

@app.route('/productstock')
def productinventory():
    with engine.connect() as connection:
        stmt = select(prodstock)
        result = connection.execute(stmt)
        stock_data = [
            {
                "product_name": row.product_name,
                "current_stock": row.current_stock,
                "minimum_stock": row.minimum_stock
            }
            for row in result
        ]
        return render_template("productinventory.html", stock_data=stock_data)

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    data = request.get_json()
    low_stock = []
    for item in data:
        stock_obj = stockmodel(item['ingredient_name'], item['current_stock'], item['minimum_stock'], item['price'])
        stock_obj.update()

    for item in data:
        current_stock = int(item['current_stock'])
        minimum_stock = int(item['minimum_stock'])
        if current_stock <= minimum_stock:
            low_stock.append(item['ingredient_name'])

    if low_stock:
        email_inventory(low_stock)
    return redirect(url_for('admin'))

@app.route('/update_product_inventory', methods=['POST'])
def update_stock_inventory():
    data = request.get_json()
    low_stock = []
    for item in data:
        stock_obj = productstockmodel(item['ingredient_name'], item['current_stock'], item['minimum_stock'])
        stock_obj.update()

    for item in data:
        current_stock = int(item['current_stock'])
        minimum_stock = int(item['minimum_stock'])
        if current_stock <= minimum_stock:
            low_stock.append(item['ingredient_name'])

    if low_stock:
        email_stock(low_stock)
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)