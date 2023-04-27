from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY, Date, Time, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class Staff(Base):
    """Represents a staff member in the database."""

    __tablename__ = 'Staffs'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey(
        'Admins.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, default=func.now())


class FaceEncoding(Base):
    """Represents the face encoding data for a staff member in the database."""

    __tablename__ = 'FaceEncodings'

    staff_id = Column(Integer, ForeignKey(
        'Staffs.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    face_encoding = Column(ARRAY(Float), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, default=func.now())


class Admin(Base):
    """Represents an admin user in the database."""

    __tablename__ = "Admins"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, default=func.now())


class Attendance(Base):
    """Represents the attendance of a staff member in an event in the database."""

    __tablename__ = "Attendances"

    id = Column(Integer, primary_key=True, nullable=False)
    event = Column(String, nullable=False)
    staff_id = Column(Integer, ForeignKey('Staffs.id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('Admins.id'), nullable=False)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, default=func.now())
