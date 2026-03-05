from sqlalchemy import insert, Table, MetaData
from connection import engine

metadata = MetaData()
students = Table('students', metadata, autoload_with=engine)

query = insert(students).values([
    {'name': 'Rahul', 'age': 22, 'city': 'Delhi'},
    {'name': 'Priya', 'age': 23, 'city': 'Mumbai'},
    {'name': 'Aman', 'age': 19, 'city': 'Gurgaon'}
])

with engine.connect() as conn:
    conn.execute(query)
    conn.commit()

print('Inserted 3 student records successfully')
