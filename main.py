import sqlite3
conn=sqlite3.connect("bank.db")
cursor=conn.cursor()

print("=" * 40)
print("     BANK MANAGEMENT SYSTEM")
print("=" * 40)
print("Welcome to Bank Management System")

print("=" * 40)
print("     BANK MANAGEMENT SYSTEM")
print("=" * 40)

while True:
    print("\n===== MAIN MENU =====")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n===== CREATE ACCOUNT =====")
            # Name
        while True:
            name = input("Enter Full Name: ")
            if name.isalpha():
                break
            print("Invalid Name!")


        while True:
            phone = input("Enter Phone Number: ")
            if phone.isdigit() and len(phone) == 10:
                break
            print("Invalid Phone Number!")


        while True:
            pin = input("Enter 4-digit PIN: ")
            if pin.isdigit() and len(pin) == 4:
                break
            print("Invalid PIN!")

        while True:
            balance = input("Enter Initial Deposit: ")
            if balance.isdigit() and int(balance)>0:
                balance=int(balance)
                break
        print("Reached")

        cursor.execute(
            "INSERT INTO accounts(name, phone, pin, balance) VALUES (?, ?, ?, ?)",
            (name, phone, pin, balance)
        )
        conn.commit()
        cursor.execute("SELECT * FROM accounts")
        print(cursor.fetchall())
        print("\nAccount Created Successfully!")
        print("Name :", name)
        print("Phone :", phone)
        print("Balance :", balance)

    elif choice == "2":

        print("\n===== LOGIN =====")

        login_phone = input("Enter Phone Number: ")
        login_pin = input("Enter PIN: ")
        cursor.execute(
            "SELECT * FROM accounts WHERE "
            "phone = ? AND pin = ?",
            (login_phone, login_pin)
        )
        account=cursor.fetchone()

        if account:
            id,name,phone,pin,balance=account
            print("\nLogin Successful!")
        else:
            print("\nInvalid Phone number or PIN!")

        while True:
                print("\n===== BANK MENU =====")
                print("1. Check Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Logout")
                print("5. Account details")

                option = input("Enter your choice: ")

                if option == "1":
                    print("Current Balance:", balance)

                elif option == "2":
                    amount = int(input("Enter Deposit Amount: "))

                    if amount > 0:
                        balance += amount
                        cursor.execute(
                            "UPDATE accounts SET balance = ? WHERE phone = ?",
                              (balance, login_phone)
                        )
                        conn.commit()

                        cursor.execute(
                         "INSERT INTO  transactions(phone, type, amount,balance) VALUES (?, ?, ?, ?)",
                        (login_phone, "Deposit", amount, balance)
                        )

                        conn.commit()

                        
                        
                        print("Amount Deposited Successfully!")
                        print("Current Balance:", balance)
                    else:
                        print("Invalid Amount!")

                elif option == "3":
                    amount = int(input("Enter Withdraw Amount: "))

                    if amount > 0 and amount <= balance:
                        balance -= amount
                        cursor.execute(
                        "UPDATE accounts SET balance = ? WHERE phone = ?",
                            (balance, login_phone)
                        )
                        conn.commit()

                        cursor.execute(
                         "INSERT INTO  transactions(phone, type, amount,balance) VALUES (?, ?, ?, ?)",
                            (login_phone, "Withdraw", amount, balance)
                             )
                        
                        conn.commit()
                        


                        print("Amount Withdrawn Successfully!")
                        print("Current Balance:", balance)
                    else:
                        print("Insufficient Balance or Invalid Amount!")

                elif option == "4":
                    print("Logged Out Successfully!")
                    break

                elif option == "5":
                    print("\n===== ACCOUNT DETAILS =====")
                    print("Name :", name)
                    print("Phone :", phone)
                    print("Balance :", balance)

                else:
                    print("Invalid Choice!")

    elif choice == "3":
            print("Thank you for using Bank Management System.")
            break

    else:
        print("Invalid choice. Please try again.")
conn.close()