from pydantic import BaseModel, EmailStr
from datetime import datetime


class StaffBase(BaseModel):
    name: str
    email: EmailStr
    gender: str
    phone_number: str


class CreateStaff(StaffBase):
    pass
    

class CreateStaffOut(StaffBase):   
    id: str
    
    created_at: datetime
    class Config():
        orm_mode = True



class StaffOut(StaffBase):
    created_at: datetime

    class Config():
        orm_mode = True
    

class StaffAllOut(StaffBase):
    id: str
    created_at: datetime

    class Config():
        orm_mode = True


class AdminCreate(BaseModel):
    email: EmailStr
    password: str


class AdminOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        orm_mode = True


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id : str | None = None 