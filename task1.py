import hashlib
import getpass
import decimal

class ATM:
    def __init__(self):
        self.users = {}
        self.logged_in_user = None

    def _get_credentials(self):
        """Gets username, password, and PIN from user."""
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        pin = input("Enter your 4-digit PIN: ")
        return username, password, pin

    def _validate_password(self, password: str) -> bool:
        """Checks if password meets requirements (length, special characters)."""
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return False
        if not any(char.isupper() for char in password):
            print("Password must contain at least one uppercase letter.")
            return False
        if not any(char.islower() for char in password):
            print("Password must contain at least one lowercase letter.")
            return False
        if not any(char.isdigit() for char in password):
            print("Password must contain at least one digit.")
            return False
        if not any(char in "!@#$%^&*()_" for char in password):
            print("Password must contain at least one special character.")
            return False
        return True

    def _validate_pin(self, pin: str) -> bool:
        """Checks if PIN is 4 digits."""
        if len(pin) != 4 or not pin.isdigit():
            print("Invalid PIN. Please use 4 digits.")
            return False
        return True

    def create_account(self) -> None:
        """Creates a new user account."""
        username, password, pin = self._get_credentials()
        
        if not self._validate_password(password):
            return
        
        if not self._validate_pin(pin):
            return
        
        if username in self.users:
            print("Username already exists.")
            return
        
        self.users[username] = {
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "pin": hashlib.sha256(pin.encode()).hexdigest(),
            "balance": decimal.Decimal(0),
            "logged_in": False,
            "transaction_history": []
        }
        print("Account created successfully.")

    def login(self) -> None:
        """Logs user into their account."""
        username, password, pin = self._get_credentials()
        
        if username not in self.users:
            print("Username does not exist.")
            return
        
        user_data = self.users[username]
        
        if hashlib.sha256(password.encode()).hexdigest() != user_data["password"]:
            print("Invalid password.")
            return
        
        if hashlib.sha256(pin.encode()).hexdigest() != user_data["pin"]:
            print("Invalid PIN.")
            return
        
        user_data["logged_in"] = True
        self.logged_in_user = username
        print("Login successful.")

    def logout(self) -> None:
        """Logs user out of their account."""
        self.users[self.logged_in_user]["logged_in"] = False
        self.logged_in_user = None
        print("You have been logged out.")

    def check_balance(self) -> None:
        """Displays user's current balance."""
        if self.logged_in_user:
            print(f"Your current balance is: ${self.users[self.logged_in_user]['balance']:.2f}")
        else:
            print("Please login first.")

    def withdraw(self) -> None:
        """Allows user to withdraw funds."""
        if self.logged_in_user:
            amount = decimal.Decimal(input("Enter withdrawal amount: $"))
            if amount > self.users[self.logged_in_user]["balance"]:
                print("Insufficient funds.")
            else:
                self.users[self.logged_in_user]["balance"] -= amount
                self.users[self.logged_in_user]["transaction_history"].append(f"Withdrawal: -${amount:.2f}")
                print(f"Withdrawal successful. New balance: ${self.users[self.logged_in_user]['balance']:.2f}")
        else:
            print("Please login first.")

    def deposit(self) -> None:
        """Allows user to deposit funds."""
        if self.logged_in_user:
            amount = decimal.Decimal(input("Enter deposit amount: $"))
            self.users[self.logged_in_user]["balance"] += amount
            self.users[self.logged_in_user]["transaction_history"].append(f"Deposit: +${amount:.2f}")
            print(f"Deposit successful. New balance: ${self.users[self.logged_in_user]['balance']:.2f}")
        else:
            print("Please login first.")

    def transaction_history(self) -> None:
        """Displays user's transaction history."""
        if self.logged_in_user:
            print("\nTransaction History:")
            for transaction in self.users[self.logged_in_user]["transaction_history"]:
                print(transaction)
        else:
            print("Please login first.")
    def display_menu(self) -> None:
        """Displays ATM menu."""
        print("\nABC Bank ATM Menu:")
        print("1. Logout")
        print("2. Check Balance")
        print("3. Withdraw")
        print("4. Deposit")
        print("5. Transaction History")
        print("6. Exit")

def main():
    atm = ATM()
    print("Welcome to ABC Bank!")

    while True:
        try:
            print("\nABC Bank ATM Simulator")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                atm.create_account()
            elif choice == "2":
                atm.login()
                while atm.logged_in_user:
                    atm.display_menu()
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        atm.logout()
                    elif choice == "2":
                        atm.check_balance()
                    elif choice == "3":
                        atm.withdraw()
                    elif choice == "4":
                        atm.deposit()
                    elif choice == "5":
                        atm.transaction_history()
                    elif choice == "6":
                        print("Thank you for banking with ABC Bank.")
                        atm.logout()
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif choice == "3":
                print("Thank you for banking with ABC Bank.")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
