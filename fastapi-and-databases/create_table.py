from sqlalchemy import Table, Column, Integer, String, MetaData, CheckConstraint
from connection import engine

metadata = MetaData()

students = Table('students', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('age', Integer, CheckConstraint('age >= 18'), nullable=False),
    Column('city', String(50), nullable=True)
)

metadata.create_all(engine)
print('Students table created successfully')
