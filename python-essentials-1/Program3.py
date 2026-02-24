def main():
    # Take inputs
    name = input("Enter your name: ").strip()
    age_input = input("Enter your age: ").strip()

    # Validate and convert age
    try:
        age = int(age_input)
    except ValueError:
        print("Invalid age input")
        return

    if age < 0:
        print("Age cannot be negative")
        return

    # Greet the user
    print(f"Hello {name}")

    # Determine age category
    if age < 13:
        print("You are a Child")
    elif 13 <= age <= 17:
        print("You are a Teenager")
    elif 18 <= age <= 59:
        print("You are an Adult")
    else:  # age >= 60
        print("You are a Senior Citizen")

    # Voting eligibility
    if age >= 18:
        print("You are eligible to vote")
    else:
        print("You are not eligible to vote")


if __name__ == "__main__":
    main()