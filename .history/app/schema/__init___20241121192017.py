from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime

# User Schemas
class UserBase(BaseModel):
    phoneNumber: str = Field(..., max_length=12)
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# Contact Schemas
class ContactBase(BaseModel):
    name: str = Field(..., max_length=25)
    email: EmailStr
    phoneNumber: str = Field(..., max_length=12)
    description: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True

# Enroll Schemas
class EnrollBase(BaseModel):
    fullname: str = Field(..., max_length=30)
    email: EmailStr
    phoneNumber: str = Field(..., max_length=12)
    gender: str = Field(..., max_length=25)
    Dob: date
    membershipPlan: str = Field(..., max_length=300)
    trainers: str = Field(..., max_length=55)
    reference: str = Field(..., max_length=55)
    address: str
    paymentStatus: Optional[str] = Field(None, max_length=55)
    price: Optional[int] = None
    dueDate: Optional[datetime] = None

class EnrollCreate(EnrollBase):
    pass

class EnrollResponse(EnrollBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Trainer Schemas
class TrainerBase(BaseModel):
    name: str = Field(..., max_length=55)
    gender: str = Field(..., max_length=20)
    phone: str = Field(..., max_length=12)
    salary: int

class TrainerCreate(TrainerBase):
    pass

class TrainerResponse(TrainerBase):
    id: int

    class Config:
        from_attributes = True

# MembershipPlan Schemas
class MembershipPlanBase(BaseModel):
    plan: str = Field(..., max_length=55)
    price: int

class MembershipPlanCreate(MembershipPlanBase):
    pass

class MembershipPlanResponse(MembershipPlanBase):
    id: int

    class Config:
        from_attributes = True

# Gallery Schemas
class GalleryBase(BaseModel):
    title: str = Field(..., max_length=100)
    img: str

class GalleryCreate(GalleryBase):
    pass

class GalleryResponse(GalleryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    phoneNumber: str = Field(..., max_length=12)
    login: str = Field(..., max_length=100)
    logout: str = Field(..., max_length=100)
    selectWorkout: str = Field(..., max_length=100)
    trainedBy: str = Field(..., max_length=100)

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int
    selectDate: date

    class Config:
        from_attributes = True