from tkinter import *
from tkinter import messagebox
import sqlite3
current_account = None

def show_balance():
    global current_account

    balance = current_account[4]
    messagebox.showinfo(
        "Bank Balance",
        f"Your Balance is Rs.{balance}"
    )
def deposit_money(amount_entry):
    try:
        amount = int(amount_entry.get())

        if amount<=0:
            messagebox.showerror("Error",
                                 "Amount must be greater than 0")
            return
    except ValueError:
        messagebox.showerror("Error",
                             "Please enter a valid amount")
        return

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE phone = ?",
        (amount, current_account[2])
    )

    cursor.execute(
    "INSERT INTO transactions (phone, type, amount) VALUES (?, ?, ?)",
    (current_account[2], "Deposit", amount)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Money Deposited Successfully!")

def deposit():
    deposit_window = Toplevel(window)
    deposit_window.title("Deposit Money")
    deposit_window.geometry("300x200")

    Label(
        deposit_window,
        text="Enter Amount",
        font=("Arial", 12)
    ).pack(pady=10)

    amount_entry = Entry(
        deposit_window,
        font=("Arial", 12)
    )
    amount_entry.pack(pady=10)

    Button(
        deposit_window,
        text="Deposit",
        font=("Arial", 12),
        command=lambda:
        deposit_money(amount_entry)
    ).pack(pady=10)

def withdraw_money(amount_entry):
    amount = int(amount_entry.get())

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    current_balance = current_account[4]

    if amount > current_balance:
        messagebox.showerror("Error", "Insufficient Balance")
    else:
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE phone = ?",
            (amount, current_account[2])
        )

        
        cursor.execute(
    "INSERT INTO transactions (phone, type, amount) VALUES (?, ?, ?)",
    (current_account[2], "Withdraw", amount)
)

        conn.commit()

        messagebox.showinfo("Success", "Money Withdrawn Successfully")

    conn.close()

def withdraw():
    withdraw_window = Toplevel(window)
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("300x200")

    Label(
        withdraw_window,
        text="Enter Amount",
        font=("Arial", 12)
    ).pack(pady=10)

    amount_entry = Entry(
        withdraw_window,
        font=("Arial", 12)
    )
    amount_entry.pack(pady=10)

    Button(
        withdraw_window,
        text="Withdraw",
        font=("Arial", 12),
        command=lambda: withdraw_money(amount_entry)
    ).pack(pady=10)

def transaction_history():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT type, amount FROM transactions WHERE phone=?",
        (current_account[2],)
    )

    records = cursor.fetchall()

    history = ""

    for row in records:
        history += f"{row[0]} : ₹{row[1]}\n"

    if history == "":
        history = "No Transactions"

    messagebox.showinfo("Transaction History", history)

    conn.close()

def logout(dashboard):
    dashboard.destroy()
    window.deiconify()

def show_account_details():
    phone=str(current_account[2])
    masked_phone="*"*6+phone[-4:]

    name = current_account[1]
    phone = masked_phone
    account_id = current_account[0]

    messagebox.showinfo(
        "Account Details",
        f"Account ID: {account_id}\n"
        f"Name: {name}\n"
        f"Phone: {phone}"
    )

def update_pin(current_pin_entry, new_pin_entry, pin_window):
    current_pin = current_pin_entry.get()
    new_pin = new_pin_entry.get()

    if current_pin == str(current_account[3]):

        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute(
        "UPDATE accounts SET pin = ? WHERE id = ?",
        (new_pin, current_account[0])
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "PIN changed successfully!"
        )

        pin_window.destroy()
    else:
        messagebox.showerror("Error", "Current PIN is incorrect")

def change_pin():
    pin_window = Toplevel(window)
    pin_window.title("Change PIN")
    pin_window.geometry("300x250")

    Label(
        pin_window,
        text="Current PIN",
        font=("Arial", 12)
    ).pack(pady=5)

    current_pin_entry = Entry(
        pin_window,
        show="*",
        font=("Arial", 12)
    )
    current_pin_entry.pack(pady=5)

    Label(
        pin_window,
        text="New PIN",
        font=("Arial", 12)
    ).pack(pady=5)

    new_pin_entry = Entry(
        pin_window,
        show="*",
        font=("Arial", 12)
    )
    new_pin_entry.pack(pady=5)

    Button(
        pin_window,
        text="Change PIN",
        font=("Arial", 12),
        command=lambda:update_pin(
            current_pin_entry,
            new_pin_entry,
            pin_window
        )
    ).pack(pady=15)

def save_account(name_entry, phone_entry, pin_entry, deposit_entry, account_window):

    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    pin = pin_entry.get().strip()
    deposit = deposit_entry.get().strip()

    # Check empty fields
    if not name or not phone or not pin or not deposit:
        messagebox.showerror("Error", "Please fill all fields")
        return

    # Check name
    if not name.isalpha():
        messagebox.showerror("Error", "Name must contain only letters")
        return

    # Check phone number
    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit phone number")
        return

    # Check PIN
    if not pin.isdigit() or len(pin) != 4:
        messagebox.showerror("Error", "PIN must contain exactly 4 digits")
        return

    # Check deposit
    try:
        deposit = int(deposit)

        if deposit < 0:
            messagebox.showerror(
                "Error",
                "Initial deposit cannot be negative"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter a valid initial deposit"
        )
        return

    # Save account in database
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO accounts (name, phone, pin, balance)
        VALUES (?, ?, ?, ?)
        """,
        (name, phone, pin, deposit)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Account Created Successfully!"
    )

    account_window.destroy()

def create_account():
    account_window = Toplevel(window)
    account_window.title("Create Account")
    account_window.geometry("350x400")

    Label(
        account_window,
        text="Create New Account",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    Label(account_window, text="Name").pack()
    name_entry = Entry(account_window)
    name_entry.pack(pady=5)

    Label(account_window, text="Phone Number").pack()
    phone_entry = Entry(account_window)
    phone_entry.pack(pady=5)

    Label(account_window, text="PIN").pack()
    pin_entry = Entry(account_window, show="*")
    pin_entry.pack(pady=5)

    Label(account_window, text="Initial Deposit").pack()
    deposit_entry = Entry(account_window)
    deposit_entry.pack(pady=5)

    Button(
        account_window,
        text="Create Account",
        command=lambda: save_account(
            name_entry,
            phone_entry,
            pin_entry,
            deposit_entry,
            account_window
        )
    ).pack(pady=20)

def open_dashboard():
    dashboard = Toplevel(window)
    dashboard.configure(bg="#0B1F3A")
    dashboard.title("Dashboard")
    dashboard.geometry("400x400")

    Label(
        dashboard,
        text=f"🏦 Welcome, {current_account[1]}",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    Button(
    dashboard,
    text="💰 Check Balance",
    font=("Arial", 12),
    width=20,
    bg="#1E88E5",
    fg="white",
    command=show_balance
    ).pack(pady=5)

    Button(
    dashboard,
    text="➕ Deposit",
    font=("Arial", 12),
    width=20,
    bg="#1E88E5",
    fg="white",
    command=deposit()
    ).pack(pady=5)

    Button(
    dashboard,
    text="➖ Withdraw",
    font=("Arial", 12),
    width=20,
    bg="#1E88E5",
    fg="white",
    command=withdraw
    ).pack(pady=5)

    Button(
    dashboard,
    text="📄 Transaction History",
    font=("Arial", 12),
    width=20,
    bg="#1E88E5",
    fg="white",
    command=transaction_history
    ).pack(pady=5)

    Button(
    dashboard,
    text="🚪 Logout",
    font=("Arial", 12),
    width=20,
    bg="#1E88E5",
    fg="white",
    command=lambda:
    logout(dashboard)
    ).pack(pady=5)

    Button(
    dashboard,
    text="👤 Account Details",
    font=("Arial", 12),
    width=20,
    bg="#1E88E5",
    fg="white",
    command=show_account_details
    ).pack(pady=5)

    Button(
        dashboard,
        text="CHANGE PIN",
        font=("Arial",12),
        width=20,
         bg="#1E88E5",
        fg="white",
        command=change_pin
    ).pack(pady=5)

def check_login(phone_entry, pin_entry,login):
    phone = phone_entry.get()
    pin = pin_entry.get()

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM accounts WHERE phone = ? AND pin = ?",
        (phone, pin)
    )

    account = cursor.fetchone()

    global current_account
    current_account = account

    if account:
        print("Login Successful!")
        login.destroy() #close the login window
        window.withdraw() 
        open_dashboard()
    else:
        print("Invalid Phone Number or PIN")

    conn.close()



def open_login():
    print("Login button clicked")
    login = Toplevel(window)
    login.title("Login")
    login.geometry("350x300")

    Label(login, text="Phone Number", font=("Arial", 12)).pack(pady=5)
    phone_entry = Entry(login, font=("Arial", 12))
    phone_entry.pack()

    Label(login, text="PIN", font=("Arial", 12)).pack(pady=5)
    pin_entry = Entry(login, font=("Arial", 12), show="*")
    pin_entry.pack()

    Button(
    login,
    text="Login",
    command=lambda: 
    check_login(phone_entry, pin_entry,login)
).pack(pady=20)

window = Tk()
window.configure(bg="#0B1F3A")

window.title("Bank Management System")
window.geometry("500x500")
window.resizable(False,False)

heading = Label(
    window,
    text="🏦 Bank Management System",
    font=("Arial", 20, "bold")
)

heading.pack(pady=20)




login_button = Button(
    window,
    text="Login",
    font=("Arial", 14),
    width=20,
    height=2,
    bg="#1E88E5",
    fg="white",
    command=open_login
)

login_button.pack(pady=10)

create_button = Button(
    window,
    text="Create Account",
    font=("Arial", 14),
    width=20,
    height=2,
    bg="#1E88E5",
    fg="white",
    command=create_account
)

create_button.pack(pady=10)


window.mainloop()