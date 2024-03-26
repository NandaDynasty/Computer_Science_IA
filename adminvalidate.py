from sqlalchemy import select
from models.adminmodels import admins
from engine import engine


def validateadmincredentials(email, password):
    with engine.connect() as connection:
        stmt = select(admins.password).where(admins.email == email)
        result = connection.execute(stmt).fetchone()
        if result:
            if password == result.password:
                return True
            else:
                return False
        else:
            return False
