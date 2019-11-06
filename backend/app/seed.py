import csv
from sqlalchemy import create_engine, Table, Column, Integer, MetaData

engine = create_engine('sqlite:///test.db', echo=True)

metadata = MetaData()
# Define the table with sqlalchemy:
my_table = Table('MyTable', metadata,
    Column('foo', Integer),
    Column('bar', Integer),
)
metadata.create_all(engine)
insert_query = my_table.insert()

# Or read the definition from the DB:
# metadata.reflect(engine, only=['MyTable'])
# my_table = Table('MyTable', metadata, autoload=True, autoload_with=engine)
# insert_query = my_table.insert()

# Or hardcode the SQL query:
# insert_query = "INSERT INTO MyTable (foo, bar) VALUES (:foo, :bar)"

with open('test.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"foo": row[0], "bar": row[1]}
            for row in csv_reader]
    )
