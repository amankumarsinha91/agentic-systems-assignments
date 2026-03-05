from pydantic import BaseModel, EmailStr, Field, validator

class Address(BaseModel):
    city: str = Field(..., min_length=3)
    pincode: str = Field(..., regex=r"^\d{6}$")  # exactly 6 digits
    
class User(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    age: int = Field(..., ge=18)  # minimum 18
    address: Address
    is_premium: bool = False

    class Config:
        validate_assignment = True  # enables assignment validation