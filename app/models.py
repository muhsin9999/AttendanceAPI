from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY, Date, Time
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
    admin_id = Column(Integer, ForeignKey('Admins.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
     
    


class FaceEncoding(Base):
    __tablename__ = 'FaceEncodings'

    
    staff_id = Column(Integer, ForeignKey('Staffs.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    face_encoding = Column(ARRAY(Float), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
     
    
    

class Admin(Base):
    __tablename__ = "Admins" 


    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class Attendance(Base):
    __tablename__ = "Attendances"

    id = Column(Integer, primary_key=True, nullable=False)
    event = Column(String, nullable=False)
    staff_id = Column(Integer, ForeignKey('Staffs.id'), nullable=False)
    event_date = Column(Date)
    event_time = Column(Time)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))