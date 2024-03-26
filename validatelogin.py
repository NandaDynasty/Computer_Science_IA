from sqlalchemy import select
from models.customersmodels import customers
from engine import engine
from werkzeug.security import check_password_hash


def validatecredentials(email, password):
    with engine.connect() as connection:
        stmt = select(customers.password).where(customers.email == email)
        result = connection.execute(stmt).fetchone()
        if result:
            hashed_password = result.password
            if check_password_hash(hashed_password, password):
                return True
            else:
                return False
        else:
            return False

