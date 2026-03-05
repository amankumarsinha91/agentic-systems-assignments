from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:password@localhost/student_db')
print('Database connection created successfully')
