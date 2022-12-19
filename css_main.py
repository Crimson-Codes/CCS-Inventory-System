import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from css_config import PHOTO_DIRECTORY
from PIL import ImageTk, Image
import pymysql
import css_config

# ====== Inventory GUI MAIN Frame and Functions ======


def inventory_frame():
    root2 = Tk()
    root2.title("CCS Admin: Inventory System")
    root2.geometry("1080x400")
    my_tree = ttk.Treeview(root2)
    storeName = "CCS Inventory System"

    def database_error(err):
        messagebox.showinfo("Error", err)
        return False

    def reverse(tuples):
        new_tup = tuples[::-1]
        return new_tup

    def insert(id, name, price, quantity):

        try:
            con = pymysql.connect(host=css_config.DB_SERVER, port=4306,
                                  user=css_config.DB_USER,
                                  password=css_config.DB_PASS,
                                  database=css_config.DB)
            cursor = con.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_inventory(itemId TEXT, itemName TEXT, itemPrice TEXT,
                 itemQuantity TEXT)""")

            cursor.execute(
                "INSERT INTO tbl_inventory VALUES ('" + str(id) + "','" + str(name) + "','" + str(price) + "','" +
                str(quantity) + "')")

            con.commit()

            entryId.delete(0, END)
            entryName.delete(0, END)
            entryPrice.delete(0, END)
            entryQuantity.delete(0, END)

        except pymysql.ProgrammingError as e:
            database_error(e)
        except pymysql.DataError as e:
            database_error(e)
        except pymysql.IntegrityError as e:
            database_error(e)
        except pymysql.NotSupportedError as e:
            database_error(e)
        except pymysql.OperationalError as e:
            database_error(e)
        except pymysql.InternalError as e:
            database_error(e)

    def delete(data):

        con = pymysql.connect(host=css_config.DB_SERVER, port=4306,
                              user=css_config.DB_USER,
                              password=css_config.DB_PASS,
                              database=css_config.DB)

        cursor = con.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS 
            tbl_inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

        cursor.execute("DELETE FROM tbl_inventory WHERE itemId = '" + str(data) + "'")
        con.commit()

        messagebox.showinfo("Database", "Data Deleted Successfully.", parent=root2)

        entryId.delete(0, END)
        entryName.delete(0, END)
        entryPrice.delete(0, END)
        entryQuantity.delete(0, END)

    def update(id, name, price, quantity, idName):

        con = pymysql.connect(host=css_config.DB_SERVER, port=4306,
                              user=css_config.DB_USER,
                              password=css_config.DB_PASS,
                              database=css_config.DB)

        cursor = con.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS 
            tbl_inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

        cursor.execute(
            "UPDATE tbl_inventory SET itemId = '" + str(id) + "', itemName = '" + str(name) + "', itemPrice = '" +
            str(price) + "', itemQuantity = '" + str(quantity) + "' WHERE itemId='" + str(idName) + "'")
        con.commit()

        messagebox.showinfo("Database", "Data Updated Successfully.", parent=root2)

        entryId.delete(0, END)
        entryName.delete(0, END)
        entryPrice.delete(0, END)
        entryQuantity.delete(0, END)

    def read():

        try:
            con = pymysql.connect(host=css_config.DB_SERVER, port=4306,
                                  user=css_config.DB_USER,
                                  password=css_config.DB_PASS,
                                  database=css_config.DB)

            cursor = con.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS 
                        tbl_inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

            cursor.execute("SELECT * FROM tbl_inventory")
            results = cursor.fetchall()

            con.commit()

            return results
            has_loaded_successfully = True

        except pymysql.InternalError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.OperationalError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.ProgrammingError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.DataError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.IntegrityError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.NotSupportedError as e:
            has_loaded_successfully = database_error(e)

        return has_loaded_successfully

    def insert_data():
        itemId = str(entryId.get())
        itemName = str(entryName.get())
        itemPrice = str(entryPrice.get())
        itemQuantity = str(entryQuantity.get())
        if itemId == "" or itemName == " ":
            messagebox.showinfo("Error", "Error Inserting Id")
        if itemName == "" or itemName == " ":
            messagebox.showinfo("Error", "Error Inserting Name")
        if itemPrice == "" or itemPrice == " ":
            messagebox.showinfo("Error", "Error Inserting Price")
        if itemQuantity == "" or itemQuantity == " ":
            messagebox.showinfo("Error", "Error Inserting Quantity")
        else:
            insert(str(itemId), str(itemName), str(itemPrice), str(itemQuantity))
            messagebox.showinfo("Database", "Data Inserted Successfully.", parent=root2)

        for data in my_tree.get_children():
            my_tree.delete(data)

        for result in reverse(read()):
            my_tree.insert(parent='', index='end', iid=result, text="", values=result, tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE')
        my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    def delete_data():
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        delete(deleteData)

        for data in my_tree.get_children():
            my_tree.delete(data)

        for result in reverse(read()):
            my_tree.insert(parent='', index='end', iid=result, text="", values=result, tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE')
        my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    def update_data():
        selected_item = my_tree.selection()[0]
        update_name = my_tree.item(selected_item)['values'][0]
        update(entryId.get(), entryName.get(), entryPrice.get(), entryQuantity.get(), update_name)

        for data in my_tree.get_children():
            my_tree.delete(data)

        for result in reverse(read()):
            my_tree.insert(parent='', index='end', iid=result, text="", values=result, tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE')
        my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

# ====== Inventory System MAIN GUI Frame ======

    titleLabel = Label(root2, text=storeName, font=('Arial bold', 30), bd=2)
    titleLabel.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

    idLabel = Label(root2, text="ID", font=('Arial bold', 15))
    nameLabel = Label(root2, text="Name", font=('Arial bold', 15))
    priceLabel = Label(root2, text="Price", font=('Arial bold', 15))
    quantityLabel = Label(root2, text="Quantity", font=('Arial bold', 15))
    idLabel.grid(row=1, column=0, padx=10, pady=10)
    nameLabel.grid(row=2, column=0, padx=10, pady=10)
    priceLabel.grid(row=3, column=0, padx=10, pady=10)
    quantityLabel.grid(row=4, column=0, padx=10, pady=10)

    entryId = Entry(root2, width=25, bd=5, font=('Arial bold', 15))
    entryName = Entry(root2, width=25, bd=5, font=('Arial bold', 15))
    entryPrice = Entry(root2, width=25, bd=5, font=('Arial bold', 15))
    entryQuantity = Entry(root2, width=25, bd=5, font=('Arial bold', 15))
    entryId.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
    entryName.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
    entryPrice.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
    entryQuantity.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

    buttonEnter = Button(
        root2, text="Enter", padx=5, pady=5, width=5,
        bd=3, font=('Arial', 15), bg="#EEEEEE", command=insert_data)
    buttonEnter.grid(row=5, column=1, columnspan=1)

    buttonUpdate = Button(
        root2, text="Update", padx=5, pady=5, width=5,
        bd=3, font=('Arial', 15), bg="#EEEEEE", command=update_data)
    buttonUpdate.grid(row=5, column=2, columnspan=1)

    buttonDelete = Button(
        root2, text="Delete", padx=5, pady=5, width=5,
        bd=3, font=('Arial', 15), bg="#EEEEEE", command=delete_data)
    buttonDelete.grid(row=5, column=3, columnspan=1)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial bold', 15))

    my_tree['columns'] = ("ID", "Name", "Price", "Quantity")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=100)
    my_tree.column("Name", anchor=W, width=200)
    my_tree.column("Price", anchor=W, width=150)
    my_tree.column("Quantity", anchor=W, width=150)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Name", text="Name", anchor=W)
    my_tree.heading("Price", text="Price", anchor=W)
    my_tree.heading("Quantity", text="Quantity", anchor=W)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=None, text="", values=result, tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    root2.mainloop()

# ====== Login SECTION GUI Functions ======


def clear_input():
    global UserEnter
    global UserPass

    UserEnter.set('')
    UserPass.set('')


def admin_check():
    global UserEnter
    global UserPass

    if UserEnter.get() == "Admin" and UserPass.get() == "CCS2020":
        messagebox.showinfo("Login Notification", "Admin Login Successful.", parent=root)
        inventory_frame()
    else:
        messagebox.showinfo("Login Notification", "Incorrect Admin Login Credentials, please try again.")


# ====== Login MAIN GUI Frame ======

root = Tk()
root.geometry("1366x768+0+0")
root.title("Crimson Computer Services Inventory Admin")
root.configure(background='#DC143C')

Tops = Frame(root, width=1366, height=100, bd=14, relief="raised")
Tops.place(x=0, y=0)

Tops.configure(background='white')

lblInfo = tk.Label(Tops, font="Arial 35 bold", text="                     Crimson Comserv Inventory Login "
                                                    "                      ")
lblInfo.grid(row=0, column=0)

# ====== Login SECTION GUI Frame ======

f2 = Frame(root, width=440, height=650, bd=8, relief="raised")
f2.place(x=900, y=300)

lblGuide_User = Label(f2, font="Arial 20 bold", text="USERNAME:", bd=2, anchor='w')
lblGuide_User.grid(row=0, column=0, sticky=W)

lblGuide_Pass = Label(f2, font="Arial 20 bold", text="PASSWORD:", bd=2, anchor='w')
lblGuide_Pass.grid(row=2, column=0, sticky=W)

ImageLogo = ImageTk.PhotoImage(Image.open(PHOTO_DIRECTORY))
lblImageLogo = Label(root, image=ImageLogo, borderwidth=0)
lblImageLogo.place(x=100, y=150)

UserEnter = tk.StringVar()
UserPass = tk.StringVar()

UserEnter_Frame2 = Entry(f2, width=25, font="Arial 20 bold", textvariable=UserEnter)
UserEnter_Frame2.grid(row=1, column=0)

UserPass_Frame2 = Entry(f2, width=25, font="Arial 20 bold", textvariable=UserPass)
UserPass_Frame2.grid(row=3, column=0)
UserPass_Frame2.config(show="*")

ClearButton = Button(f2, font="Arial 16 bold", text="Clear", command=clear_input)
ClearButton.grid(row=5, column=0, sticky=W)

LoginButton = Button(f2, font="Arial 16 bold", text="Login", command=admin_check)
LoginButton.grid(row=5, column=0, sticky=E)

root.mainloop()
