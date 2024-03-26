from sqlalchemy import create_engine

connection_string = "mysql+mysqlconnector://root:squashF1#172@127.0.0.1:3306/isira"

engine = create_engine(connection_string, echo=True)