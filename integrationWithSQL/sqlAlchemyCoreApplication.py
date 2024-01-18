from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import engine

engine = create_engine('sqlite:///:memory')

metadata_obj = MetaData()
user = Table(
    'user', metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(60)),
    Column('nickname', String(50), nullable=False)
)

user_prefs = Table(
    'user_prefs', metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))
)

print("Info da tabela user_prefs")
print(user_prefs.primary_key)
print(user_prefs.foreign_keys)

for table in metadata_obj.sorted_tables:
    print(table)

metadata_obj.create_all(engine)

metadata_db_obj = MetaData(schema='bank')
financial_info = Table(
    'financial_info',
    metadata_db_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False)
)

print("\nInfo da tabela financial_info")
print(financial_info.primary_key)
print(financial_info.foreign_keys)

print('\nExecutando statement sql')
sql = text('select * from user')
result = engine.execute(sql)
for row in result:
    print(row)

print(engine.execute(sql))