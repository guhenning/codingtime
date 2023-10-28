import requests


from_currency = input("Enter the source currency (e.g., USD): ").upper()
to_currency = input("Enter the target currency (e.g., EUR): ").upper()
amount = float(input("Enter the amount to convert: "))


response = requests.get(
    f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
)

if response.status_code == 200:
    print(
        f"{amount} {from_currency} is {response.json()['rates'][to_currency]} {to_currency}"
    )

else:
    print("Connection Error")
