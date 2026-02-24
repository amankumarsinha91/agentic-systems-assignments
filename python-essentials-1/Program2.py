def main():
    fname = input("Enter First name: ").strip()
    lname = input("Enter last name: ").strip()
    age_input = input("Enter age: ").strip()
    try:
        age = int(age_input)
    except ValueError:
        print("Invalid age input")
        return

    
    if age < 0:
        print("Age cannot be negative")
        return

    # Print full name using string concatenation
    full_name = "Full Name: " + fname + " " + lname
    print(full_name)

    # Print age next year
    print("You will be " + str(age + 1) + " next year")


if __name__ == "__main__":
    main()