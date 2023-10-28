import string
import secrets


def generate_password(length=12, max_length=25):
    symbols = "&*%$#@!"
    characters = string.ascii_letters + string.digits + symbols
    length = min(length, max_length)  # Ensure length doesn't exceed max_length
    secure_password = "".join(secrets.choice(characters) for _ in range(length))
    return secure_password


def main():
    num_passwords = int(input("Enter the number of passwords to generate: "))
    password_length = int(
        input("Enter the desired password length (up to 25 characters): ")
    )

    for i in range(1, num_passwords + 1):
        password = generate_password(password_length)
        print(f"Random Password {i}: {password}")


if __name__ == "__main__":
    main()
