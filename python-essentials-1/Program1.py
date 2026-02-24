def main():
    try:
        a = int(input("Enter first number ").strip())
        b = int(input("Enter second number ").strip())
    except ValueError:
        print("Invalid input")
        return
    print("sum:",a+b)

    if(b==0):
        print("Cannot divide by zero")
    else:
        print("Division:",a/b)

if __name__ == "__main__":
    main()
