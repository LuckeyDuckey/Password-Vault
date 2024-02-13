from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_list = []

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(self.key)

    def load_key(self, key):
        self.key = key

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for i in initial_values:
                self.add_password(i[0], i[1], i[2])

    def load_password_file(self, path):
        self.password_file = path
        self.password_list = []

        with open(path, "r") as f:
            for line in f:
                site, username, password = line.split(":")
                self.password_list.append([site, Fernet(self.key).decrypt(username.encode()).decode(), Fernet(self.key).decrypt(password.encode()).decode()])

    def add_password(self, site, username, password):
        self.password_list.append([site, username, password])

        if self.password_file is not None:
            with open(self.password_file, "a+") as f:
                username_encypted = Fernet(self.key).encrypt(username.encode())
                password_encypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + username_encypted.decode() + ":" + password_encypted.decode() + "\n")

    def remove_password(self, name):
        with open(self.password_file, 'r') as f:
            lines = f.readlines()
        
        with open(self.password_file, "w") as f:
            for line in lines:
                if line.split(":")[0] != name:
                    f.write(line)

    def edit_password(self, name, new_password):
        with open(self.password_file, 'r') as f:
            lines = f.readlines()
        
        with open(self.password_file, "w") as f:
            for line in lines:
                if line.split(":")[0] != name:
                    f.write(line)
                else:
                    username_encypted = Fernet(self.key).encrypt(new_password[1].encode())
                    password_encypted = Fernet(self.key).encrypt(new_password[2].encode())
                    f.write(new_password[0] + ":" + username_encypted.decode() + ":" + password_encypted.decode() + "\n")

    def get_password(self):
        return self.password_list
  
pm = PasswordManager()

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import random, string

root = Tk()
root.title("Password Manager")
root.geometry("750x625")
root.resizable(False, False)

letters = string.ascii_letters + string.digits + "!£$%^&*()_+{}[]-=#@,.<>?"

passwords = []

Key = "Qsjjh3cEd7KeUoG86IuhWB6FxhMWzg3dYqFAKDQiL1E=" # You will want to ask the user to input this

def show_passwords():
    global passwords
    #tree.delete(*tree.get_children())
    for i in tree.get_children():
        tree.delete(i)
    pm.load_key(key.get("1.0","end-1c"))#("5XY1-AWhCwuXXj23iJzuT9ozY8_TKJuNCZtL-K9zbiY=")key.get("1.0","end-1c")
    pm.load_password_file("mypassword.pass")
    passwords = pm.get_password()
    for i in passwords:
        tree.insert("", "end", text="1", values=(i[0], i[1], i[2]))

def edit_selected():
    if len(tree.selection()) > 0:
        selected = tree.selection()
        pm.edit_password(tree.item(tree.selection())["values"][0], [platform.get("1.0","end-1c"), username.get("1.0","end-1c"), password.get("1.0","end-1c")])
        passwords[passwords.index(tree.item(selected)['values'])] = [platform.get("1.0","end-1c"), username.get("1.0","end-1c"), password.get("1.0","end-1c")]
        tree.item(selected, values=([platform.get("1.0","end-1c"), username.get("1.0","end-1c"), password.get("1.0","end-1c")]))

def remove_selected():
    if len(tree.selection()) > 0:
        passwords.remove(tree.item(tree.selection())["values"])
        pm.remove_password(tree.item(tree.selection())["values"][0])
        tree.delete(tree.selection())

def add():
    tree.insert('', 'end', text="1", values=(platform.get("1.0","end-1c"), username.get("1.0","end-1c"), password.get("1.0","end-1c")))
    passwords.append([platform.get("1.0","end-1c"), username.get("1.0","end-1c"), password.get("1.0","end-1c")])
    pm.add_password(platform.get("1.0","end-1c"), username.get("1.0","end-1c"), password.get("1.0","end-1c"))

s = ttk.Style()
#s.theme_use('default')

tree = ttk.Treeview(root, column=("c1", "c2", "c3"), show="headings", height=25, selectmode="browse")

tree.column("# 1", width=240)
tree.heading("# 1", text="Platform")
tree.column("# 2", width=240)
tree.heading("# 2", text="Username")
tree.column("# 3", width=240)
tree.heading("# 3", text="Password")

tree.pack(pady=10)

# Insert the data in Treeview widget
for i in passwords:
    tree.insert("", "end", text="1", values=(i[0], i[1], i[2]))

Button(root, text="Add Password", command=add, bd=3).place(x=10,y=550)
Button(root, text="Remove Password", command=remove_selected, bd=3).place(x=105,y=550)
Button(root, text="Edit Password", command=edit_selected, bd=3).place(x=222,y=550)
Button(root, text="Show All Password", command=show_passwords, bd=3).place(x=625,y=550)

key = Text(root, height=1, width=15)
key.place(x=490,y=556)
key.insert("1.0", Key)

platform = Text(root, height=1, width=15)
platform.place(x=65,y=590)
platform.insert("1.0", "platform")

username = Text(root, height=1, width=15)
username.place(x=260,y=590)
username.insert("1.0", "Luckey_Duckey")

password = Text(root, height=1, width=15)
password.place(x=450,y=590)
password.insert("1.0", "".join(random.choice(letters) for i in range(10)))

Label(root, text="Platform").place(x=10,y=590)
Label(root, text="Username").place(x=195,y=590)
Label(root, text="Password").place(x=390,y=590)
Label(root, text="Master Password").place(x=390,y=556)

root.mainloop()
