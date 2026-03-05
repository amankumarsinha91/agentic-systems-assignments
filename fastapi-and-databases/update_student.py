from sqlalchemy import update, Table, MetaData
from connection import engine

metadata = MetaData()
students = Table('students', metadata, autoload_with=engine)

query = update(students).where(students.c.name == 'Rahul').values(city='Noida')

with engine.connect() as conn:
    conn.execute(query)
    conn.commit()

print('Updated city for student Rahul')
