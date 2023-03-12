from sqlalchemy import Column, Integer, Text, ForeignKey
from base import Base


# class User(Base):
#     __tablename__ = 'User'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(Text)
#     password = Column(Text)

#     def __repr__(self) -> str:
#         return str((self.id, self.username, self.password))

class PizzaBase(Base):
    __tablename__ = 'Base'

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    def __repr__(self) -> str:
        return str((self.id, self.name))

class Pizza(Base):
    __tablename__ = 'Pizza'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    base_id = Column(Integer, ForeignKey('Base.id'))

    def __repr__(self) -> str:
        return str((self.id, self.name, self.description, self.base_id))