import smtplib
from datetime import datetime
from email.message import EmailMessage
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import select

from engine import engine
from models.productmodels import products


def email_inventory(items):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "kavyaanand07@gmail.com"
    sender_password = "dpmmuesttokxwfxz"
    recipient_email = "kavyaanand07@gmail.com"
    subject = "Items to be reordered"
    low_stock = '\n'.join(items)
    body = f'These are the items you need to reorder: \n{low_stock}'
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = recipient_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, em.as_string())

def email_order_details(email, cart_data):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "kavyaanand07@gmail.com"
    sender_password = "dpmmuesttokxwfxz"
    recipient_email = email
    subject = "Your Order Confirmation"
    email_body = MIMEMultipart()
    email_body['From'] = sender_email
    email_body['To'] = recipient_email
    email_body['Subject'] = subject
    max_product_name_length = max(len(item["item"]) for item in cart_data)

    email_text = f"Dear customer, thank you for placing an order with us. Please find the details of your order below. Regards, \nThe Isira team.\nProduct{' ' * (max_product_name_length - 7)}Quantity\n{'-' * (max_product_name_length + 10)}------------\n"

    total_price = 0
    for item in cart_data:
        product_name = item["item"]
        quantity = item["quantity"]
        email_text += f"{product_name:{max_product_name_length}} {quantity}\n"
        with engine.connect() as connection:
            stmt = select(products.price).where(products.product_name == product_name)
            price = connection.execute(stmt).fetchone()
            price = price[0]
            total_price = total_price + price

    email_text += f"\nTotal Price: Rs. {total_price:.2f}"
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email_text += f"\nOrder Date: {order_date}"

    email_body.attach(MIMEText(email_text, 'plain'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, email_body.as_string())

def email_order_admin(cart_data):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "kavyaanand07@gmail.com"
    sender_password = "dpmmuesttokxwfxz"
    recipient_email = "kavyaanand07@gmail.com"
    subject = "Order has been placed"
    email_body = MIMEMultipart()
    email_body['From'] = sender_email
    email_body['To'] = recipient_email
    email_body['Subject'] = subject
    max_product_name_length = max(len(item["item"]) for item in cart_data)

    email_text = f"Product{' ' * (max_product_name_length - 7)}Quantity\n{'-' * (max_product_name_length + 10)}------------\n"

    total_price = 0
    for item in cart_data:
        product_name = item["item"]
        quantity = item["quantity"]
        email_text += f"{product_name:{max_product_name_length}} {quantity}\n"
        with engine.connect() as connection:
            stmt = select(products.price).where(products.product_name == product_name)
            price = connection.execute(stmt).fetchone()
            price = price[0]
            total_price = total_price + price

    email_text += f"\nTotal Price: Rs. {total_price:.2f}"
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email_text += f"\nOrder Date: {order_date}"

    email_body.attach(MIMEText(email_text, 'plain'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, email_body.as_string())

def email_order_admin(cart_data):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "kavyaanand07@gmail.com"
    sender_password = "dpmmuesttokxwfxz"
    recipient_email = "kavyaanand07@gmail.com"
    subject = "Order has been placed"
    email_body = MIMEMultipart()
    email_body['From'] = sender_email
    email_body['To'] = recipient_email
    email_body['Subject'] = subject
    max_product_name_length = max(len(item["item"]) for item in cart_data)

    email_text = f"Product{' ' * (max_product_name_length - 7)}Quantity\n{'-' * (max_product_name_length + 10)}------------\n"

    total_price = 0
    for item in cart_data:
        product_name = item["item"]
        quantity = item["quantity"]
        email_text += f"{product_name:{max_product_name_length}} {quantity}\n"
        with engine.connect() as connection:
            stmt = select(products.price).where(products.product_name == product_name)
            price = connection.execute(stmt).fetchone()
            price = price[0]
            total_price = total_price + price

    email_text += f"\nTotal Price: Rs. {total_price:.2f}"
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email_text += f"\nOrder Date: {order_date}"

    email_body.attach(MIMEText(email_text, 'plain'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, email_body.as_string())

def email_stock(items):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "kavyaanand07@gmail.com"
    sender_password = "dpmmuesttokxwfxz"
    recipient_email = "kavyaanand07@gmail.com"
    subject = "Out of stock products"
    low_stock = '\n'.join(items)
    body = f'These are the products that are out of stock: \n{low_stock}'
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = recipient_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, em.as_string())

def preparation_notification(email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "kavyaanand07@gmail.com"
    sender_password = "dpmmuesttokxwfxz"
    recipient_email = email
    subject = "Order Status Update"
    body = "Dear Customer, thank you for placing an order with us.\nThis email is to inform you that your order is now being prepared. You will be notified when it is dispatched. Thank you.\nRegards,\nThe Isira team"
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = recipient_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, em.as_string())

def dispatch_notification(email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "kavyaanand07@gmail.com"
    sender_password = "dpmmuesttokxwfxz"
    recipient_email = email
    subject = "Order Status Update"
    body = "Dear Customer, thank you for placing an order with us.\nThis email is to inform you that your order has been dispatched. Thank you.\nRegards,\nThe Isira team"
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = recipient_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, recipient_email, em.as_string())



