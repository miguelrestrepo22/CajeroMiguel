import tkinter as tk
from tkinter import messagebox
import sqlite3
from getpass import getpass
import tkinter.simpledialog as simpledialog
class ATM:
    def __init__(self, master):
        self.master = master
        self.master.title("Cajero Automático")
        
        self.create_database()
        
        self.create_widgets()
        
        self.logged_in = False
        self.current_user = None
        self.check_logged_in()
    
    def create_database(self):
        self.conn = sqlite3.connect("atm.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            password TEXT,
                            balance REAL DEFAULT 0
                            )""")
        self.conn.commit()
    
    def create_widgets(self):
        self.label_username = tk.Label(self.master, text="Nombre de usuario:")
        self.label_username.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_username = tk.Entry(self.master)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        
        self.label_password = tk.Label(self.master, text="Contraseña:")
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        
        self.button_create_account = tk.Button(self.master, text="Crear cuenta", command=self.create_account)
        self.button_create_account.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        
        self.button_login = tk.Button(self.master, text="Iniciar sesión", command=self.login)
        self.button_login.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        self.button_deposit = tk.Button(self.master, text="Depositar", command=self.deposit, state="disabled")
        self.button_deposit.grid(row=4, column=0, padx=10, pady=5)
        
        self.button_withdraw = tk.Button(self.master, text="Retirar", command=self.withdraw, state="disabled")
        self.button_withdraw.grid(row=4, column=1, padx=10, pady=5)
        
        self.label_balance = tk.Label(self.master, text="")
        self.label_balance.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
    
    def create_account(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
        if self.cur.fetchone():
            messagebox.showerror("Error", "El nombre de usuario ya existe. Por favor, elija otro.")
        else:
            self.cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Éxito", "La cuenta ha sido creada con éxito.")
    
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cur.fetchone()
        
        if user:
            self.logged_in = True
            self.current_user = user
            self.button_create_account.config(state="disabled")
            self.button_login.config(state="disabled")
            self.button_deposit.config(state="normal")
            self.button_withdraw.config(state="normal")
            self.label_balance.config(text=f"Saldo actual: {user[3]}")
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
    
    def deposit(self):
        amount = float(tk.simpledialog.askstring("Depositar", "Ingrese la cantidad a depositar:"))
        if amount > 0:
            self.cur.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, self.current_user[0]))
            self.conn.commit()
            self.refresh_balance()
        else:
            messagebox.showerror("Error", "Ingrese una cantidad válida para depositar.")
    
    def withdraw(self):
        amount = float(tk.simpledialog.askstring("Retirar", "Ingrese la cantidad a retirar:"))
        if amount > 0 and amount <= self.current_user[3]:
            self.cur.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, self.current_user[0]))
            self.conn.commit()
            self.refresh_balance()
        else:
            messagebox.showerror("Error", "Ingrese una cantidad válida para retirar.")
    
    def refresh_balance(self):
        self.cur.execute("SELECT * FROM users WHERE id=?", (self.current_user[0],))
        user = self.cur.fetchone()
        self.label_balance.config(text=f"Saldo actual: {user[3]}")
    
    def check_logged_in(self):
        self.cur.execute("SELECT * FROM users")
        if self.cur.fetchone():
            self.button_create_account.config(state="normal")
            self.button_login.config(state="normal")
        else:
            messagebox.showwarning("Advertencia", "No hay cuentas registradas en la base de datos. Por favor, cree una cuenta.")

root = tk.Tk()
app = ATM(root)
root.mainloop()
