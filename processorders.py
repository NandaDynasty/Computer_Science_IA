import datetime

from sqlalchemy import select, desc, and_

from engine import engine
from models.productmodels import products
from models.customersmodels import customers
from models.ordersmodels import orders, ordermodel
from models.revenuemodels import monthlyrevenue, mrmodel
from models.orderpricemodels import opmodel
from models.cakerevenuemodel import cakerevenue, crmodel
from models.breadrevenuemodel import breadrevenue, brmodel
from models.morerevenuemodel import morerevenue, moremodel
from models.savouryrevenuemodel import savouryrevenue, srmodel
from models.prodstockmodels import prodstock, productstockmodel
from notifications import email_stock


def process_orders(cart_data, user_email):
    with engine.connect() as connection:
        orders_query = select(orders.order_id).order_by(desc(orders.order_id)).limit(1)
        order_id = connection.execute(orders_query).fetchone()
        if order_id:
            order_id = order_id.order_id + 1
        else:
            order_id = 1
    order_price = 0
    total_price = 0
    for item in cart_data:
        product_name = item['item']
        quantity = item['quantity']
        with engine.connect() as connection:
            date = datetime.date.today()
            month_name = date.strftime('%B')
            year_name = date.strftime('%Y')
            stmt = select(monthlyrevenue).where(
                and_(monthlyrevenue.year == year_name, monthlyrevenue.month == month_name))
            result = connection.execute(stmt).fetchone()

            if result:
                tr = result.total_revenue
                quantity = int(quantity)
                stmt = select(products.price).where(products.product_name == product_name)
                price = connection.execute(stmt).fetchone()
                price = price[0]
                tr = tr + (quantity * price)
                revenue_obj = mrmodel(month_name, year_name, tr)
                revenue_obj.update()

            else:
                quantity = int(quantity)
                stmt = select(products.price).where(products.product_name == product_name)
                price = connection.execute(stmt).fetchone()
                price = price[0]
                tr = quantity * price
                revenue_obj = mrmodel(month_name, year_name, tr)
                revenue_obj.insert()

            stmt = select(products.product_type).where(products.product_name == product_name)
            type = connection.execute(stmt).fetchone()
            type = type[0]
            if type == "Cake":
                stmt = select(cakerevenue).where(and_(cakerevenue.year == year_name, cakerevenue.month == month_name))
                result = connection.execute(stmt).fetchone()
                if result:
                    cr = result.revenue
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    cr = cr + (quantity * price)
                    cr_obj = crmodel(month_name, year_name, cr)
                    cr_obj.update()
                else:
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    cr = quantity * price
                    cr_obj = crmodel(month_name, year_name, cr)
                    cr_obj.insert()
            elif type == "Bread":
                stmt = select(breadrevenue).where(
                    and_(breadrevenue.year == year_name, breadrevenue.month == month_name))
                result = connection.execute(stmt).fetchone()
                if result:
                    br = result.revenue
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    br = br + (quantity * price)
                    br_obj = brmodel(month_name, year_name, br)
                    br_obj.update()
                else:
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    br = quantity * price
                    br_obj = brmodel(month_name, year_name, br)
                    br_obj.insert()
            elif type == "Savoury":
                stmt = select(savouryrevenue).where(
                    and_(savouryrevenue.year == year_name, savouryrevenue.month == month_name))
                result = connection.execute(stmt).fetchone()
                if result:
                    sr = result.revenue
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    sr = sr + (quantity * price)
                    sr_obj = srmodel(month_name, year_name, sr)
                    sr_obj.update()
                else:
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    sr = quantity * price
                    sr_obj = srmodel(month_name, year_name, sr)
                    sr_obj.insert()
            elif type == "More":
                stmt = select(morerevenue).where(and_(morerevenue.year == year_name, morerevenue.month == month_name))
                result = connection.execute(stmt).fetchone()
                if result:
                    mr = result.revenue
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    mr = mr + (quantity * price)
                    mr_obj = moremodel(month_name, year_name, mr)
                    mr_obj.update()
                else:
                    quantity = int(quantity)
                    stmt = select(products.price).where(products.product_name == product_name)
                    price = connection.execute(stmt).fetchone()
                    price = price[0]
                    mr = quantity * price
                    mr_obj = moremodel(month_name, year_name, mr)
                    mr_obj.insert()
            if type != "Cake":
                stmt = select(prodstock).where(prodstock.product_name == product_name)
                stock = connection.execute(stmt).fetchone()
                current = stock.current_stock
                minimum = stock.minimum_stock
                quantity = int(quantity)
                current = current - quantity
                stock_obj = productstockmodel(product_name, current, minimum)
                stock_obj.update()

            stmt = select(products.product_id, products.price).where(products.product_name == product_name)
            product_id = connection.execute(stmt).fetchone()
            total_price = total_price + product_id.price
            product_id = product_id.product_id
            stmt = select(customers.customer_id).where(customers.email == user_email)
            customer_id = connection.execute(stmt).fetchone()
            customer_id = customer_id.customer_id
            order_obj = ordermodel(order_id, product_id, customer_id, quantity, date)
            order_obj.insert()
            stmt = select(products.price).where(products.product_name == product_name)
            price = connection.execute(stmt).fetchone()
            price = price[0]
            quantity = int(quantity)
            order_price = order_price + price * quantity
    op_obj = opmodel(order_id, order_price)
    op_obj.insert()
    low_stock = []
    with engine.connect() as connection:
        stmt = select(prodstock.current_stock, prodstock.minimum_stock, products.product_name). \
            join(products, prodstock.product_name == products.product_name). \
            where(products.product_type != "Cake")
        low_stock_items = connection.execute(stmt).fetchall()

        for item in low_stock_items:
            product_name = item.product_name
            current_stock = item.current_stock
            minimum_stock = item.minimum_stock

            if current_stock < minimum_stock:
                low_stock.append(product_name)
    if low_stock:
        email_stock(low_stock)

