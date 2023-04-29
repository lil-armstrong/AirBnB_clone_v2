from sqlalchemy import create_engine, inspect
import models

user = 'hbnb_dev'
password = 'hbnb_dev_pwd'
host = 'localhost'
database = 'hbnb_dev_db'

engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{database}')
inspector = inspect(engine)

table_names = inspector.get_table_names()

for table_name in table_names:
    print(f'Table name: {table_name}')
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f'\tColumn name: {column["name"]}')
