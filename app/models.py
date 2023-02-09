from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base



class Staff(Base):
    __tablename__ = 'Staffs'

    id = Column(Integer, primary_key=True, nullable=False) 
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    


class Image(Base):
    __tablename__ = 'Images'

    staff_id = Column(Integer, ForeignKey('Staffs.id', ondelete="CASCADE"), primary_key = True, nullable=False)
    filename = Column(String, unique=True)
    file_data = Column(LargeBinary) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    

class Admin(Base):
    __tablename__ = "Admins"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))