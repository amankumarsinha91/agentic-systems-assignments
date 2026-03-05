from sqlalchemy import delete, Table, MetaData
from connection import engine

metadata = MetaData()
students = Table('students', metadata, autoload_with=engine)

query = delete(students).where(students.c.age < 20)

with engine.connect() as conn:
    conn.execute(query)
    conn.commit()

print('Deleted students with age < 20')
