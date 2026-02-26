from pydantic import BaseModel, Field, EmailStr, field_validator

class UserRegister(BaseModel):
    username: str = Field(..., min_length=5)
    email: EmailStr
    age: int = Field(..., ge=18)

    # Optional: extra validator for username if needed
    @field_validator('username')
    def validate_username(cls, value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value

    # Optional age validator (Pydantic's ge=18 already covers this)
    @field_validator('age')
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Age must be at least 18")
        return value
    
    @field_validator('email')
    @classmethod 
    def email_validator(cls, value): 
        domain_name= value.split('@')[-1]
        print(" domain_name : "+ domain_name)
        if domain_name != 'masai.com':
            raise ValueError("Not a valid domain")   
        return value
    
# Create User Dictionary
user_info_dict = {"username":"amankumar", "email":"aman@masai.com", "age":22}

user = UserRegister(**user_info_dict)
print(user)
