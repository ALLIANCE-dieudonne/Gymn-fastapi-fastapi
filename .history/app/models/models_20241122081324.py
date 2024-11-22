from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.db.mixins import TimestampMixin
from sqlalchemy import text
from datetime import datetime


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column(String(12), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Contact(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    email = Column(String, nullable=False)
    phoneNumber = Column(String(12), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return f"<Contact {self.email}>"

class Enroll(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(30), nullable=False)
    email = Column(String, nullable=False)
    phoneNumber = Column(String(12), nullable=False)
    gender = Column(String(25), nullable=False)
    Dob = Column(Date, nullable=False)
    membershipPlan = Column(String(300), nullable=False)
    trainers = Column(String(55), nullable=False)
    reference = Column(String(55), nullable=False)
    address = Column(Text, nullable=False)
    paymentStatus = Column(String(55), nullable=True)
    price = Column(Integer, nullable=True)
    dueDate = Column(DateTime, nullable=True)
    # timestamp is handled by TimestampMixin (created_at)

    def __repr__(self):
        return f"<Enroll {self.fullname}>"

class Trainer(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(55), nullable=False)
    gender = Column(String(20), nullable=False)
    phone = Column(String(12), nullable=False)
    salary = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Trainer {self.name}>"

class MembershipPlan(Base):
    id = Column(Integer, primary_key=True, index=True)
    plan = Column(String(55), nullable=False)
    price = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<MembershipPlan {self.id}>"

class Gallery(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    img = Column(String, nullable=False)  # Path to image
    # timestamp is handled by TimestampMixin (created_at)

    def __repr__(self):
        return f"<Gallery {self.id}>"

class Attendance(Base):
    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column(String(12), nullable=False)
    selectDate = Column(DateTime, nullable=False)
    login = Column(String(100), nullable=False)
    logout = Column(String(100), nullable=False)
    selectWorkout = Column(String(100), nullable=False)
    trainedBy = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Attendance {self.id}>"