# This program is not fully optimised and completed but I wanted to submit something

import sys
import re
import pwinput
import yfinance
import bcrypt


def main():
    print(u'\u001b[0m') # resets colour
    home_prompt()

def home_prompt():
    print('Welcome to ApplePear Bank.')
    while True:
        print('Select one of the following options:')
        option = input("(1) Help: Guide to the bank and its functions.\n(2) Account: Check your account.\n(3) Calculator: Use our financial calculator.\n(4) Stocks: Track a stock.\n(5) Quit: Exit the application.\n")
        match option.lower():
            case '1' | 'help' | 'guide':
                help_prompt()
                break
            case '2' | 'account':
                account_user_prompt()
                break
            case '3' | 'calculator' | 'financial calculator':
                calculator_prompt()
                break
            case '4' | 'stock' | 'stocks' | 'stock market':
                stock_market_prompt()
                break
            case '5' | 'quit' | 'exit':
                sys.exit('Thanks for using ApplePear Bank.')
            case _:
                print('Not a valid option. ')


def help_prompt():
    print("Here is a quick summary of the bank's features.")
    print("Account: Open a virtual bank account, deposit and withdraw money and also earn interest.")
    print("Calculator: Calculate interest and depreciation with out financial calculator.")
    print("Stocks: Keep an eye on the price of stocks.")
    while True:
        option = input('Enter the name of a feature you would like to go into more detail or leave blank to go back. ')
        match option.lower():
            case 'account':
                print('You must first create an account with your name and password. Afterwards, you are free to deposit and withdrawn money as well as pass time to earn interest.')
                print('To access the account in the future, you will be required to enter your password.')
                print('Your account details and balance will be stored in a file so you can access them in the future. (Your password is hashed for security)')
            case 'calculator':
                print('You can choose to calculate simple interest, compound interest or depreciation.')
                print('Simple interest and depreciation will be caluclated with principal, interest rate and time periods.')
                print('Compound interest will be calculated with principal, interest rate, time periods and compound rate.')
            case 'stocks':
                print('You will be prompted to enter the name of a stock and receive the current price of the stock, the price at last close as well as the percentage increase.')
            case '':
                home_prompt()
                break

def calculator_prompt():
    print('Welcome to the financial calculator.')
    while True:
        print('Would you like to:')
        option = input('(1) Use our simple interest calculator\n(2) Use our compound interest calculator\n(3) Use our depreciation calculator\n(4) Go back\n')
        match option.lower():
            case '1'|'simple':
                P = float(input('Principal: $'))
                R = float(input('Interest rate per time period (write percentage as decimal): '))/100
                N = int(input('Time periods: '))
                print(f'The interest amounts to ${calculate_simple_interest(P, R, N)}. The total amount is ${round(P*R*N+P, 2)}.')
            case '2'|'compound':
                P = float(input('Principal: $'))
                R = float(input('Interest rate per time period (write percentage as decimal): '))/100
                N = int(input('Time periods: '))
                T = int(input('Times compounded per time period: '))
                print(f'The interest amounts to ${calculate_compound_interest(P, R, N, T)}. The total amount is ${round((P*(1+(R/T))**(N*T)), 2)}.')
            case '3'|'depreciation':
                P = float(input('Principal: $'))
                R = float(input('Depreciation rate per time period (write percentage as decimal): '))/100
                N = int(input('Time periods: '))
                print(f'The depreciation amount is ${calculate_depreciation(P, R, N)}. The value after depreciation is ${round((P*(1-R)**N), 2)}.')
            case '4' | 'go back' | 'back':
                home_prompt()
                break

def calculate_simple_interest(P, R, N):
    return round(P*(R/100)*N, 2)

def calculate_compound_interest(P, R, N, T):
    return round((P*(1+((R/100)/T))**(N*T))-P, 2)

def calculate_depreciation(P, R, N):
    return round(P-(P*(1-(R/100))**N), 2)

def account_details_exists():
        try:
            open('account_details.txt','r').close()
            return True
        except FileNotFoundError:
            return False

def account_user_prompt():
    if account_details_exists():
        with open('account_details.txt', 'r') as file:
            account_details = file.readlines()
            print(f'Welcome back {account_details[0]}.')
            while True:
                pwd = pwinput.pwinput(prompt='Enter your password to access your account: ', mask='*').strip()
                if bcrypt.checkpw(pwd.encode('utf8'), account_details[1].strip().encode('utf8')):
                    break
                else:
                    print('Password is incorrect.')
            account_inside_prompt()
    else:
        print("Welcome into the bank. It appears this is your first time here.\nLet's set up your first account.")
        username = input('Name: ')
        while True:
            password, salt = password_input()
            confirm_password = pwinput.pwinput(prompt='Confirm password (Leave blank to go back): ', mask='*').strip()
            while bcrypt.hashpw(confirm_password.encode('utf8'), salt) != password:
                if confirm_password != '':
                    print(u'\u001b[31m ❌ Does not match original password.\u001b[0m')
                    confirm_password = pwinput.pwinput(prompt='Confirm password: ', mask='*').strip()
                else:
                    break
            if bcrypt.hashpw(confirm_password.encode('utf8'), salt) == password:
                break
        print("Great! Your account has been created. Let's make an initial deposit.")
        while True:
            try:
                initial_deposit = round(float(input('How much money would you like to deposit? $')), 2)
                if initial_deposit > 0:
                    break
                else:
                    print('Enter a positive number.')
            except ValueError:
                print('Enter a valid number.')

        while True:
            try:
                print('What would you like your interest rate to be per annum?')
                interest_rate = float(input('Enter a percentage as a decimal: ')) / 100
                if interest_rate > 0:
                    break
                else:
                    print('Enter a positive percentage.')
            except ValueError:
                print('Enter a valid percentage.')
        while True:
            try:
                compound_rate = int(input('How many times would you like your interest to be compounded per year? '))
                if compound_rate > 0:
                    break
                else:
                    print('Enter a positive number.')
            except ValueError:
                print('Enter a valid integer.')
        print("Great! Let's enter your account.")
        password = password.decode('utf8')
        with open('account_details.txt', 'w') as file:
            file.write(f'{username}\n{password}\n{initial_deposit}\n{interest_rate}\n{compound_rate}')
        account_inside_prompt()

def account_inside_prompt():
    with open('account_details.txt', 'r') as file:
        lines = []
        account_details = file.readlines()
        accounts = Accounts(float(account_details[2]), float(account_details[3]), int(account_details[4]))
    with open('account_details.txt', 'a+') as file:
        while True:
            print('Select one of the following options:')
            options = input('(1) Balance: Check your balance\n(2) Deposit: Deposit money\n(3) Withdraw: Withdraw money\n(4) Increment: Pass one year of time.\n(5) Go back\n')
            match options.lower():
                case '1'|'balance'|'check':
                    print(f'Your current balance is ${round(accounts.balance)}')
                case '2'|'deposit':
                    amount = float(input('How much money would you like to deposit? '))
                    accounts.deposit(amount)
                case '3'|'withdraw':
                    amount = float(input('How much money would you like to withdraw? '))
                    accounts.withdraw(amount)
                case '4'|'increment':
                    print('One year has passed.')
                    accounts.compound_interest()
                    print(f'Your new balance is ${round(accounts.balance)}')
                case '5'|'go back'|'back':
                    lines = []
                    for i, line in enumerate(file):
                        if i != 2:
                            lines.append(f'{line}\n')
                        else:
                            lines.append(f'{accounts.balance}\n')
                    file.truncate()
                    for l in lines:
                        file.write(l)
                    home_prompt()
                    break
            lines = []
            for i, line in enumerate(file):
                if i != 2:
                    lines.append(f'{line}\n')
                else:
                    lines.append(f'{accounts.balance}\n')
            file.truncate()
            for l in lines:
                file.write(l)

def password_input():
    while True:
        password = pwinput.pwinput(prompt='Password: ', mask='*').strip()
        if re.search(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf8'), salt), salt
        else:
            print('Password must have:')

            if re.search(r".{8,}", password):
                print(u'\u001b[32m ✔️  Minimum 8 characters in length\u001b[0m')
            else:
                print(u'\u001b[31m ❌ Minimum 8 characters in length\u001b[0m')

            if re.search(r".*(?=.*?[A-Z]).*", password):
                print(u'\u001b[32m ✔️  At least one uppercase English letter\u001b[0m')
            else:
                print(u'\u001b[31m ❌ At least one uppercase English letter\u001b[0m')

            if re.search(r"(?=.*?[a-z])", password):
                print(u'\u001b[32m ✔️  At least one lowercase English letter\u001b[0m')
            else:
                print(u'\u001b[31m ❌ At least one lowercase English letter\u001b[0m')

            if re.search(r"(?=.*?[0-9])", password):
                print(u'\u001b[32m ✔️  At least one digit\u001b[0m')
            else:
                print(u'\u001b[31m ❌ At least one digit\u001b[0m')

            if re.search(r"(?=.*?[#?!@$%^&*-])", password):
                print(u'\u001b[32m ✔️  At least one special character\u001b[0m')
            else:
                print(u'\u001b[31m ❌ At least one special character\u001b[0m')

def stock_market_prompt():
    while True:
        stock = input('Enter the name of a stock you want to track. ').upper()
        stocks = Stocks(stock)
        try:
            print(stocks)
            print((lambda percent: f'\u001b[32m{stock} is up by {round(percent*100, 2)}% since last close.\u001b[0m' if percent > 0 else (f'\u001b[31m{stock} is down by {round(percent*(-100), 2)}% since last close.\u001b[0m' if percent < 0 else (r'0% change since last close.')))(stocks.price_diff_since_last_close()))
            option1 = input('Select one of the following options:\n(1) Track another stock\n(2) Go back\n')
            match option1.lower():
                case '1' | '(1)' | 'track' | 'stock' | 'another' | 'again':
                    continue
                case '2' | '(2)' | 'go back' | 'back':
                    break
        except KeyError:
            print('Not a valid stock.')
    home_prompt()


class Stocks:
    def __init__(self, stock):
        self.stock = stock

    def __str__(self):
        return f'\u001b[1m{self.stock}\u001b[0m\nCurrent stock price: {self.current_stock_price()}\nStock price at last close: {self.previous_stock_price()}'

    def price_diff_since_last_close(self):
        return (self.current_stock_price() / self.previous_stock_price()) - 1

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        self._stock = stock

    def current_stock_price(self):
        stock_info = yfinance.Ticker(self.stock).info
        market_price = stock_info['regularMarketPrice']
        return market_price

    def previous_stock_price(self):
        stock_info = yfinance.Ticker(self.stock).info
        previous_close_price = stock_info['regularMarketPreviousClose']
        return previous_close_price


class Accounts:
    def __init__(self, balance=0, interest_rate=0.03, compound_rate=1):
        self._balance = balance
        self.interest_rate = interest_rate
        self.compound_rate = compound_rate

    @property
    def balance(self):
        return self._balance

    def deposit(self, n):
        if n > 0:
            self._balance += n
        else:
            print('Enter a valid positive number.')

    def withdraw(self, n):
        if self._balance-n >= 0:
            self._balance -= n
        else:
            print('Insufficient funds.')

    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, interest_rate):
        self._interest_rate = interest_rate

    @property
    def compound_rate(self):
        return self._compound_rate

    @compound_rate.setter
    def compound_rate(self, compound_rate):
        self._compound_rate = compound_rate

    def compound_interest(self):
        self._balance += self._balance * self.interest_rate


if __name__ == "__main__":
    main()
