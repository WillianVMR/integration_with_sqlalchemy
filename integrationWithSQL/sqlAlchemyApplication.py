import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import inspect, select, func
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()  # Estrutura modelo para criar as classes das minhas tabelas


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User (id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address (id={self.id}, email_address={self.email_address})"


print(User.__tablename__)
print(Address.__tablename__)

# conection with database
engine = create_engine("sqlite://")

# create class as tables in database
Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)

print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    willian = User(
        name='willian',
        fullname='willian ribeiro',
        address=[Address(email_address='teste@email.com')]
    )

    peralta = User(
        name='peralta',
        fullname='peralta monstro',
        address=[Address(email_address='peralta@email.com'), Address(email_address='segundo@email.com')]
    )

    patrick = User(name='patrick', fullname='Patrick Cardoso')

    # sending to DB (data persisting)

    session.add_all([willian, peralta, patrick])

    session.commit()

stmt = select(User).where(User.name.in_(["willian", 'peralta']))
print("Recuperando os nomes da lista")
for user in session.scalars(stmt):
    print(user)


print("\nRecuperando os endereços de email de Peralta")
stmt_address = select(Address).where(Address.user_id.in_([2]))
for address in session.scalars(stmt_address):
    print(address)


stmt_order = select(User).order_by(User.fullname.desc())
print("\nRecuperando info de maneria ordenada")
for result in session.scalars(stmt_order):
    print(result)

# Scalars pega somente o primeiro resultado
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
print("\nRealizando um join")
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):
    print(result)
