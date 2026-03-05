from pydantic import BaseModel, EmailStr, field_validator, ValidationError, Field

class Address(BaseModel):
    city: str = Field(..., min_length=3)
    # exactly 6 digits; length is enforced by Field; digits-only enforced by validator
    pincode: str = Field(..., min_length=6, max_length=6)

    @field_validator("pincode")
    @classmethod
    def check_digit(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Pincode must contain only digits")
        return v

class User(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    age: int = Field(..., ge=18)  # minimum 18
    address: Address
    is_premium: bool = False

    # Pydantic v2 config
    model_config = {
        "validate_assignment": True  # enables assignment validation
    }


def main():
    print("=== User Registration (Static Data) ===")

    try:
        # ----------- STATIC FIXED DATA ------------
        address_data = {
            "city": "ggn",
            "pincode": "122001"
        }

        user_data = {
            "user_id": 101,
            "name": "Aman Kumar",
            "email": "aman@example.com",
            "age": 25,
            "address": address_data,
            "is_premium": True
        }
        # ------------------------------------------

        # Create nested Address and User
        user = User(**user_data)

        # Print results
        print("\n User created successfully!")
        print(user)

        print("\n— As dict —")
        print(user.model_dump())

        print("\n— As JSON —")
        print(user.model_dump_json(indent=2))

        # Demonstrate assignment validation (will raise if invalid)
        # Uncomment to test:
        # user.age = 17  #  raises ValidationError due to ge=18

    except ValidationError as ve:
        print("\n Validation error:")
        # In v2, you can print JSON of errors like this:
        print(ve.json(indent=2))

    except Exception as e:
        print(f"\n Unexpected error: {e}")


if __name__ == "__main__":
    main()