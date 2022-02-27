import csv
import os  # This command will import multiple operating system tools
import tkinter as tk  # This has all the code for GUIs.
import tkinter.font as font  # This lets us use different fonts.
# import the convenience function closing for the safe closing of database cursor and connection
# import the tool to get accurate time stamp
from datetime import datetime
# import tools for image display
from PIL import ImageTk, Image
from tkinter import ttk
# import of the sqlite module
import sqlite3
from sqlite3 import Error


# This class will create records for Stock and manage operations on them
class Stock:
    def __init__(self, master):
        self.stock_master = tk.Frame(master)  # instance attribute frame for stock
        self.stock_master.config(bg='azure3')  # color set
        self.connection = sqlite3.connect("AllAboutToys.db")  # connection to db/ create
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE if not exists Stock ("  # table create
                            "toy_name TEXT, "
                            "category TEXT, "
                            "price REAL, "
                            "quantity REAL "
                            ")")

        # some inputs for the db, run once.
        # self.cursor.execute("INSERT INTO Stock1 VALUES ('Teddy', 'Soft toy', 12 , 22")
        # self.cursor.execute("INSERT INTO Stock1 VALUES ('Giraffe', 'Soft toy', 15 , 20)")
        # self.cursor.execute("INSERT INTO Stock1 VALUES ('BMW', 'Car', 10.99 , 25)")
        # self.cursor.execute("INSERT INTO Stock1 VALUES ('Mercedes', 'Car', 16.50 , 28)")
        self.connection.commit()  # accept changes and close DB
        self.connection.close()

        # open the table in treeview, add headings
        self.tree = ttk.Treeview(self.stock_master, column=("column1", "column2", "column3", "column4", "column5"),
                                 show='headings')
        self.tree.heading("#1", text="TOY NAME")
        self.tree.heading("#2", text="CATEGORY")
        self.tree.heading("#3", text="PRICE")
        self.tree.heading("#4", text="QUANTITY")
        self.tree.heading("#5", text="TOY ID")
        self.tree.grid(row=0, column=0, padx=50)
        # Entry boxes
        self.toy_name = tk.Entry(self.stock_master, width=30)
        self.toy_name.grid(row=7, column=0, pady=5)

        self.category = tk.Entry(self.stock_master, width=30)
        self.category.grid(row=9, column=0, pady=5)

        self.price = tk.Entry(self.stock_master, width=30)
        self.price.grid(row=11, column=0, pady=5)

        self.quantity = tk.Entry(self.stock_master, width=30)
        self.quantity.grid(row=13, column=0, pady=5)

        self.delete_box = tk.Entry(self.stock_master, width=30)
        self.delete_box.grid(row=21, column=0, pady=5)

        # Create labels
        self.toy_name_label = tk.Label(self.stock_master, bg='azure3', text='Toy Name')
        self.toy_name_label.grid(row=6, column=0)

        self.category_label = tk.Label(self.stock_master, bg='azure3', text='Category')
        self.category_label.grid(row=8, column=0)

        self.price_label = tk.Label(self.stock_master, bg='azure3', text='Price')
        self.price_label.grid(row=10, column=0)

        self.quantity_lbl = tk.Label(self.stock_master, bg='azure3', text='Quantity')
        self.quantity_lbl.grid(row=12, column=0)

        self.delete_lbl = tk.Label(self.stock_master, bg='azure3', text='Please enter a toy ID')
        self.delete_lbl.grid(row=20, column=0)

        # buttons to operate GUI
        add_into_table_btn = tk.Button(self.stock_master, text='Add Record to Categories Database',
                                       command=self.add)
        add_into_table_btn.grid(row=17, column=0, pady=5)

        b2 = tk.Button(self.stock_master, text="view data", command=self.display)
        b2.grid(row=15, column=0, pady=5)

        clear_table = tk.Button(self.stock_master, text='Clear All Records', command=self.remove_all)
        clear_table.grid(row=16, column=0)

        delete_btn = tk.Button(self.stock_master, text='Delete Record', command=self.delete_record)
        delete_btn.grid(row=22, column=0)

        edit_btn = tk.Button(self.stock_master, text='Edit Record', command=self.edit_record)
        edit_btn.grid(row=23, column=0)

        exit_btn = tk.Button(self.stock_master, text='Exit',
                             command=self.change_to_start)
        exit_btn.grid(row=25, columnspan=5, pady=1, padx=5, ipadx=5)

        save_btn = tk.Button(self.stock_master, text='Save to file',
                             command=self.save_to_file)
        save_btn.grid(row=5, columnspan=5, pady=1, padx=5, ipadx=5)

        self.stock_master.pack()

        # Empty instance attributes that will be used inside instance methods
        self.edit_master = None
        self.toy_name_edit = None
        self.category_edit = None
        self.price_edit = None
        self.quantity_edit = None
        self.conn = None

    # this instance method will add new item to the db and check if already exist
    def add(self):
        connect = sqlite3.connect("AllAboutToys.db")  # create/connect to db
        # cursor
        self.cursor = connect.cursor()
        # check if the input exists, if exists display 'already exist', if not add new item

        self.cursor.execute("SELECT * FROM Stock WHERE toy_name=:toy_name AND"
                            " category=:category AND price=:price AND quantity=:quantity ",
                            {
                                'toy_name': self.toy_name.get(),
                                'category': self.category.get(),
                                'price': self.price.get(),
                                'quantity': self.quantity.get(),
                            })

        # It will bring all records
        records = self.cursor.fetchall()

        if not records:
            self.cursor.execute("INSERT INTO Stock VALUES (:toy_name, :category, :price, :quantity)",
                                {
                                    'toy_name': self.toy_name.get(),
                                    'category': self.category.get(),
                                    'price': self.price.get(),
                                    'quantity': self.quantity.get(),
                                })
            self.toy_name.delete(0, tk.END)
            self.category.delete(0, tk.END)
            self.price.delete(0, tk.END)
            self.quantity.delete(0, tk.END)
            connect.commit()
            # close connection
            connect.close()

        else:
            self.already_exist()  # popup window

    # function that will display an error message
    def already_exist(self):
        master_a = tk.Toplevel(self.stock_master)  # new window
        master_a.title("Exist")  # '.title' is used to crete the title of our window
        master_a.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        master_a.configure(bg="azure3")  # This changes a color of our window
        tk.Label(master_a, bg="lightyellow", fg="black", text="Item already exist").pack()  # This display a text
        tk.Button(master_a, bg="white", fg="black", text="Exit",
                  command=master_a.destroy).pack()  # Creates a button

    # instance method that will display an error message
    def empty(self):
        master_a = tk.Toplevel(self.stock_master)  # new window
        master_a.title("Empty")  # '.title' is used to crete the title of our window
        master_a.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        master_a.configure(bg="azure3")  # This changes a color of our window
        tk.Label(master_a, bg="azure3", fg="black", text="Please enter ID").pack()  # This display a text
        tk.Button(master_a, bg="white", fg="black", text="Back",
                  command=master_a.destroy).pack()  # Creates a button

    # that instance method will display all db in treeview
    def display(self):
        self.connection = sqlite3.connect("AllAboutToys.db")  # connect to db
        cur = self.connection.cursor()
        cur.execute("SELECT toy_name, quantity FROM Stock")  # take all data from stock table
        lst_empty = []  # an empty list where products below 20 will be stored
        # this loop will take the products below 20 and append it into empty list
        for self.row in cur.fetchall():
            print(self.row[0])
            x = self.row[1]
            num = float(20)
            if x < num:  # this will check x
                lst_empty.append(self.row[0])

        self.connection.commit()  # commit changes
        self.connection.close()  # close connection
        if lst_empty:
            self.low_in_stock(lst_empty)  # this popup window will display products below 20
        else:
            self.msg_updated()  # if all products are more than 20 then update msg will appear
        self.connection = sqlite3.connect("AllAboutToys.db")  # connect to db
        cur = self.connection.cursor()
        cur.execute("SELECT *, oid FROM Stock")  # take all data from stock table
        rows = cur.fetchall()
        for row in rows:  # this will display all records on the table
            print(row)  # it print all records in the database
            self.tree.insert('', tk.END, values=row)  # insert in the treeview table

        self.connection.commit()  # commit changes
        self.connection.close()  # close connection

    # this instance method will clear the data table
    def remove_all(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

    # this instance method will take product id and delete this product from DB.
    def delete_record(self):
        connect = sqlite3.connect('AllAboutToys.db')  # create/connect to db

        # cursor
        self.cursor = connect.cursor()

        if entry := self.delete_box.get():  # check if value is in get and assign to entry box
            self.cursor.execute("DELETE from Stock WHERE oid = " + entry)

            self.delete_box.delete(0, tk.END)

            # Commit changes
            connect.commit()

        else:
            self.empty()
            # close connection
        connect.close()

    # this instance method will take product ID and bring all details about this product into a new window
    def edit_record(self):
        if entry := self.delete_box.get():  # check if value is in get and assign to entry box
            # create/connect to db
            connect = sqlite3.connect('AllAboutToys.db')
            # cursor
            cursor = connect.cursor()
            # setting the new window
            self.edit_master = tk.Toplevel(self.stock_master)  # new window
            self.edit_master.title('Update Records')  # window name
            self.edit_master.configure(bg='azure3')  # window colour
            self.edit_master.iconphoto(True,
                                       tk.PhotoImage(file="teddy-bear.png"))  # window icon
            cursor.execute("SELECT * FROM Stock WHERE oid = " + entry)  # this will take all details from the DB
            # depends on provided ID
            # It will bring all records
            records = cursor.fetchall()

            # Entry boxes

            self.toy_name_edit = tk.Entry(self.edit_master, width=30)
            self.toy_name_edit.grid(row=0, column=1, padx=20, pady=(10, 0))

            self.category_edit = tk.Entry(self.edit_master, width=30)
            self.category_edit.grid(row=1, column=1)

            self.price_edit = tk.Entry(self.edit_master, width=30)
            self.price_edit.grid(row=2, column=1, padx=20)

            self.quantity_edit = tk.Entry(self.edit_master, width=30)
            self.quantity_edit.grid(row=3, column=1, padx=20)

            # Labels
            toy_name_label = tk.Label(self.edit_master, text='Toy Name')
            toy_name_label.grid(row=0, column=0, pady=(10, 0))

            category_label = tk.Label(self.edit_master, text='Category')
            category_label.grid(row=1, column=0)

            price_label = tk.Label(self.edit_master, text='Price')
            price_label.grid(row=2, column=0)

            quantity_label = tk.Label(self.edit_master, text='Quantity')
            quantity_label.grid(row=3, column=0)

            # loop through results and put in the new window entry boxes
            for record in records:
                self.toy_name_edit.insert(0, record[0])
                self.category_edit.insert(0, record[1])
                self.price_edit.insert(0, record[2])
                self.quantity_edit.insert(0, record[3])

            update_btn = tk.Button(self.edit_master, text='Update Record',
                                   command=self.update)  # button for update()
            update_btn.grid(row=4, columnspan=5, pady=1, padx=5, ipadx=5)
            # Commit changes
            connect.commit()
            # close connection
            connect.close()
        else:
            self.empty()  # popup window

    # this instance method will update changes provided in edit window
    def update(self):
        # Connect to the DB
        connect = sqlite3.connect('AllAboutToys.db')
        # cursor
        cursor = connect.cursor()
        # variable to get the PK
        record_id = self.delete_box.get()
        # this will take the PK and update all columns that are assign to it
        cursor.execute("""UPDATE Stock SET
                                       toy_name =:toy_name,
                                       category =:category,
                                       price =:price,
                                       quantity=:quantity

                                       WHERE oid =:oid""",
                       dict(toy_name=self.toy_name_edit.get(), category=self.category_edit.get(),
                            price=self.price_edit.get(), quantity=self.quantity_edit.get(), oid=record_id))
        # Commit changes
        connect.commit()
        # close connection
        connect.close()
        # self.msg_updated()

        self.connection = sqlite3.connect("AllAboutToys.db")  # connect to db
        cur = self.connection.cursor()
        cur.execute("SELECT toy_name, quantity FROM Stock")  # take all data from stock table
        lst = []  # list with less than 20
        for self.row in cur.fetchall():   # here I will check all records and display less than 20 in stock list
            print(self.row[0])
            x = self.row[1]
            num = float(20)
            if x < num:  # this will check x
                lst.append(self.row[0])
        # Commit changes
        self.connection.commit()
        # close connection
        self.connection.close()
        # self.msg_updated()
        #
        if lst:
            self.low_in_stock(lst)
        else:
            self.msg_updated()  # this popup window will appear if more than 20

        self.edit_master.destroy()

    # instance method that displays list of less than 20 products
    def low_in_stock(self, lst=None):
        if not lst:
            lst = []
        master_l = tk.Toplevel(self.stock_master)  # new window
        master_l.title("LOW")  # '.title' is used to crete the title of our window
        master_l.geometry("300x200")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        master_l.configure(bg="azure3")  # This changes a color of our window
        tk.Label(master_l, bg="azure3", fg="black", font=("arial", 10),
                 text=f"This is a list of toy names that are low in stock: \n"
                      f"\n{lst}\n"
                      f"Less than 20 left").pack()  # this will display text plus attached list
        tk.Button(master_l, bg="white", fg="black", text="Exit",
                  command=master_l.destroy).pack()  # Creates a button

    def msg_updated(self):  # instance method that will display update message with timestamp
        master2 = tk.Toplevel(self.stock_master)  # new window
        master2.title("Data Updated")  # '.title' is used to crete the title of our window
        master2.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("Records Updated" + "\n " + "\n" + "%d/%m/%Y %H:%M:%S")
        tk.Label(master2, bg="azure3", fg="black", text=dt_string).pack()
        # This display a text. Also we can
        # change the color of our widget.
        tk.Button(master2, bg="white", fg="black", text="Back",
                  command=master2.destroy).pack()  # Creates a button
        master2.configure(bg="azure3")  # This changes a color of our window

    # this instance method will close stock frame
    def change_to_start(self):
        self.stock_master.forget()

    # this instance method will take all of the data and save it into csv file
    def save_to_file(self):
        try:
            self.conn = sqlite3.connect('AllAboutToys.db')  # DB connection
            # Export data into CSV file
            msg_label = tk.Label(self.stock_master, bg='azure3', text='"Exporting data into CSV............"')
            msg_label.grid(row=1, column=0)
            cursor = self.conn.cursor()
            cursor.execute("select * from Stock")  # select all from DB
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("Saved on" + "\n " + "\n" + "%d/%m/%Y %H:%M:%S")  # accurate date and time
            day_time = now.strftime("%d.%m.%Y_%H.%M.%S")
            file_name = f"stock_data_{day_time}.csv"  # name of the file + timestamp
            dir_path = os.path.join(os.getcwd(), file_name)  # file path plus file name
            with open(file_name, "w+") as csv_file:  # open csv file and insert data from DB
                csv_writer = csv.writer(csv_file, delimiter="\t")
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
            msg_label = tk.Label(self.stock_master, bg='azure3',
                                 text='"Data exported Successfully into {}"'.format(dir_path) + '\n' + dt_string)
            msg_label.grid(row=2, column=0)  # message that data was saved

        except Error as e:
            print(e)  # error will display if any complication will appear (in Python console)

            # Close database connection

        finally:
            self.conn.close()


# Class to create and manage Products DB
class Products:
    def __init__(self, master):
        self.products_master = tk.Frame(master)  # instance attribute that will create a frame products
        self.products_master.config(bg='azure3')  # color of product frame

        # create/connect to db
        # opening of a database connection, creates a new database if it does not exist
        self.connection = sqlite3.connect("AllAboutToys.db")
        # the cursor object is used to send SQL statements to the database
        self.cursor = self.connection.cursor()
        # Here I created the entry boxes where users will type Products details
        self.Toy_name = tk.Entry(self.products_master, width=30)
        self.Toy_name.grid(row=7, column=0, padx=50)

        self.Description = tk.Entry(self.products_master, width=30)
        self.Description.grid(row=9, column=0, padx=20)

        self.Price = tk.Entry(self.products_master, width=30)
        self.Price.grid(row=11, column=0, padx=20)

        self.delete_window = tk.Entry(self.products_master, width=30)
        self.delete_window.grid(row=21, column=0, padx=20)

        # Here I created a labels that inform what kind of data user should provide
        self.Toy_name_label = tk.Label(self.products_master, bg='azure3', text='Toy name')
        self.Toy_name_label.grid(row=6, column=0)

        self.Description_label = tk.Label(self.products_master, text='')
        self.Description_label = tk.Label(self.products_master, bg='azure3', text='Description')
        self.Description_label.grid(row=8, column=0)

        self.Price_label = tk.Label(self.products_master, bg='azure3', text='Price')
        self.Price_label.grid(row=10, column=0)

        self.delete_lbl = tk.Label(self.products_master, bg='azure3', text='Please enter toy ID')
        self.delete_lbl.grid(row=18, column=0)

        # buttons to operate GUI
        self.add_into_table_btn = tk.Button(self.products_master, text='Add Record to Products Database',
                                            command=self.add)
        self.add_into_table_btn.grid(row=17, columnspan=5, pady=1, padx=5, ipadx=5)

        self.display_btn = tk.Button(self.products_master, text='Display Records',
                                     command=self.display)
        self.display_btn.grid(row=15, columnspan=5, pady=1, padx=5, ipadx=5)

        self.delete_btn = tk.Button(self.products_master, text='Delete Record',
                                    command=self.delete)
        self.delete_btn.grid(row=22, columnspan=5, pady=1, padx=5, ipadx=5)

        self.edit_btn = tk.Button(self.products_master, text='Edit Record',
                                  command=self.edit)
        self.edit_btn.grid(row=24, columnspan=5, pady=1, padx=5, ipadx=5)

        self.exit_btn = tk.Button(self.products_master, text='Exit',
                                  command=self.change_to_start)
        self.exit_btn.grid(row=25, columnspan=5, pady=1, padx=5, ipadx=5)

        self.remove_all_btn = tk.Button(self.products_master, text='Clear Records',
                                        command=self.remove_all)
        self.remove_all_btn.grid(row=16, columnspan=5, pady=1, padx=5, ipadx=5)

        # open the table in treeview, add headings
        self.tree = ttk.Treeview(self.products_master, column=("column1", "column2", "column3", "column4"),
                                 show='headings')
        self.tree.heading("#1", text="TOY NAME")
        self.tree.heading("#2", text="DESCRIPTION")
        self.tree.heading("#3", text="PRICE")
        self.tree.heading("#4", text="TOY ID")
        self.tree.grid(row=0, column=0, padx=50)

        # Create a table. Ignore if table already exist in DB.

        self.cursor.execute("CREATE TABLE if not exists Products ("
                            "Toy_name TEXT, "
                            "Description TEXT, "
                            "Price REAL"
                            ")")

        self.products_master.pack()

        # Empty instance attributes that will be used and defined inside instance methods
        self.edit_master = None
        self.toy_name_edit = None
        self.description_edit = None
        self.price_edit = None

    # this instance method will clear out the treeview table
    def remove_all(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

    # this instance method will display popup window. It will be used in further instance methods
    def empty(self):
        master_a = tk.Toplevel(self.products_master)  # new window assign to the products frame
        master_a.title("Empty")  # '.title' is used to crete the title of our window
        master_a.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        master_a.configure(bg="azure3")  # This changes a color of our window
        tk.Label(master_a, bg="azure3", fg="black", text="Please enter ID").pack()  # This display a text
        tk.Button(master_a, bg="white", fg="black", text="Back", command=master_a.destroy).pack()  # Creates a button

    def already_exist(self):  # instance method that will display an error message
        master2 = tk.Toplevel(self.products_master)  # new window
        master2.title("Exist")  # '.title' is used to crete the title of our window
        master2.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        tk.Label(master2, bg="azure3", fg="black", text="Item already exist").pack()  # This display a text
        tk.Button(master2, bg="white", fg="black", text="Exit", command=master2.destroy).pack()  # Creates a button
        master2.configure(bg="azure3")  # This changes a color of our window

    # Instance method to add new Product into Products DB
    def add(self):
        connect = sqlite3.connect('AllAboutToys.db')  # create/connect to db
        # cursor
        self.cursor = connect.cursor()
        # I executed the cursor to run operations on the Products table
        # I pick the columns names that will be fill in
        self.cursor.execute("SELECT * FROM Products WHERE Toy_name=:Toy_name AND"
                            " Description=:Description AND Price=:Price ",
                            {
                                'Toy_name': self.Toy_name.get(),  # here I took the info from entry windows
                                'Description': self.Description.get(),
                                'Price': self.Price.get()
                            })
        # It will bring all records
        records = self.cursor.fetchall()

        if not records:
            self.cursor.execute("INSERT INTO Products VALUES (:Toy_name, :Description, :Price)",
                                {
                                    'Toy_name': self.Toy_name.get(),
                                    'Description': self.Description.get(),
                                    'Price': self.Price.get(),
                                })
            self.Toy_name.delete(0, tk.END)  # this code will clear the boxes after user add an item
            self.Description.delete(0, tk.END)
            self.Price.delete(0, tk.END)
            # Commit changes
            connect.commit()
            # close connection
            connect.close()
        else:
            self.already_exist()

    # this instance method will display all records inside the table
    def display(self):
        self.connection = sqlite3.connect("AllAboutToys.db")  # connect to db
        cur = self.connection.cursor()
        cur.execute("SELECT *, oid FROM Products")  # take all data from stock table
        rows = cur.fetchall()  # this will bring up all data
        for row in rows:
            print(row)  # it print all records in the database
            self.tree.insert('', tk.END, values=row)  # insert in the treeview table
        self.connection.commit()  # commit changes
        self.connection.close()  # close connection

    # this instance method will take the Product ID and delete product from DB
    def delete(self):
        connect = sqlite3.connect('AllAboutToys.db')  # create/connect to db
        # cursor
        self.cursor = connect.cursor()
        if entry := self.delete_window.get():  # check if value is in get and assign to entry box
            # code that will take PK and delete the data from the table
            self.cursor.execute("DELETE from Products WHERE oid = " + entry)
            # this code will clear the window
            self.delete_window.delete(0, tk.END)
            # Commit changes
            connect.commit()
            # close connection
        else:
            self.empty()
        # close connection
        connect.close()

    # this instance method will take product ID and display information about this product in the new window
    # user will be able to edit it there
    def edit(self):
        if entry := self.delete_window.get():  # check if value is in get and assign to entry box
            self.edit_master = tk.Toplevel(self.products_master)  # New window for edit
            self.edit_master.title('Update Records')  # title of the new window
            self.edit_master.configure(bg='azure3')  # background
            self.edit_master.iconphoto(True,
                                       tk.PhotoImage(file="teddy-bear.png"))  # icon
            # create/connect to db
            connect = sqlite3.connect('AllAboutToys.db')
            # cursor
            self.cursor = connect.cursor()
            # this code will bring up existed data to the window
            self.cursor.execute("SELECT * FROM Products WHERE oid = " + entry)
            # It will bring all records
            records = self.cursor.fetchall()

            # Empty entry windows for our new screen
            self.toy_name_edit = tk.Entry(self.edit_master, width=30)
            self.toy_name_edit.grid(row=0, column=1, padx=20, pady=(10, 0))

            self.description_edit = tk.Entry(self.edit_master, width=30)
            self.description_edit.grid(row=1, column=1)

            self.price_edit = tk.Entry(self.edit_master, width=30)
            self.price_edit.grid(row=2, column=1, padx=20)

            # Labels for our new screen
            toy_name_label = tk.Label(self.edit_master, text='Toy Name')
            toy_name_label.grid(row=0, column=0, pady=(10, 0))

            description_label = tk.Label(self.edit_master, text='Description')
            description_label.grid(row=1, column=0)

            price_label = tk.Label(self.edit_master, text='Price')
            price_label.grid(row=2, column=0)

            # loop through results and bring them to the new window
            for self.record in records:
                self.toy_name_edit.insert(0, self.record[0])
                self.description_edit.insert(0, self.record[1])
                self.price_edit.insert(0, self.record[2])

            update_btn = tk.Button(self.edit_master, text='Update Record',
                                   command=self.update)  # update button for update()
            update_btn.grid(row=4, columnspan=5, pady=1, padx=5, ipadx=5)
            # Commit changes
            connect.commit()
            # close connection
            connect.close()
        else:
            self.empty()  # popup window

    # instance method to display popup window
    def msg_updated(self):
        master2 = tk.Toplevel(self.products_master)  # new window
        master2.title("Data Updated")  # '.title' is used to crete the title of our window
        master2.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("Records Updated" + "\n " + "\n" + "%d/%m/%Y %H:%M:%S")
        tk.Label(master2, bg="azure3", fg="black", text=dt_string).pack()
        # This display a text. Also we can
        # change the color of our widget.
        tk.Button(master2, bg="white", fg="black", text="Back",
                  command=master2.destroy).pack()  # Creates a button
        master2.configure(bg="azure3")  # This changes a color of our window

    # this instance methode will update the records that are edited inside edit() window
    def update(self):
        # Connect to the DB
        connect = sqlite3.connect('AllAboutToys.db')
        # cursor
        self.cursor = connect.cursor()
        # variable to get the PK
        record_id = self.delete_window.get()
        # this will take the PK and update all columns that are assign to it
        self.cursor.execute("""UPDATE Products SET
                                    Toy_name =:Category,
                                    Description =:Toy,
                                    Price =:Age

                                    WHERE oid =:oid""",
                            dict(Category=self.toy_name_edit.get(), Toy=self.description_edit.get(),
                                 Age=self.price_edit.get(), oid=record_id))

        # Commit changes
        connect.commit()
        # close connection
        connect.close()
        self.msg_updated()
        # this will close the window
        self.edit_master.destroy()

    # this instance method will close the frame
    def change_to_start(self):
        self.products_master.forget()


# Class to create and manage Categories DB
class Categories:
    def __init__(self, master):
        self.categories_master = tk.Frame(master)  # instance attribute frame
        self.categories_master.config(bg='azure3')  # color set for frame
        # create/connect to db
        # opening of a database connection, creates a new database if it does not exist
        self.connection = sqlite3.connect("AllAboutToys.db")
        # the cursor object is used to send SQL statements to the database
        self.cursor = self.connection.cursor()
        # Here I created an entry boxes where users can type.
        self.Category_name = tk.Entry(self.categories_master, width=30)
        self.Category_name.grid(row=7, column=0, padx=50)

        self.Toy_name = tk.Entry(self.categories_master, width=30)
        self.Toy_name.grid(row=9, column=0, padx=20)

        self.age = tk.Entry(self.categories_master, width=30)
        self.age.grid(row=11, column=0, padx=20)

        self.delete_window = tk.Entry(self.categories_master, width=30)
        self.delete_window.grid(row=21, column=0, padx=20)

        # Labels that will be assign to the windows.
        self.Category_name_label = tk.Label(self.categories_master, bg='azure3', text='Category Name')
        self.Category_name_label.grid(row=6, column=0)

        self.Toy_name_label = tk.Label(self.categories_master, bg='azure3', text='Toy Name')
        self.Toy_name_label.grid(row=8, column=0)

        self.age_label = tk.Label(self.categories_master, bg='azure3', text='Age group')
        self.age_label.grid(row=10, column=0)

        self.delete_lbl = tk.Label(self.categories_master, bg='azure3', text='Please enter toy ID')
        self.delete_lbl.grid(row=20, column=0)
        # empty instance attributes that will be used further in instance methods for this class
        self.edit_master = None
        self.category_name_edit = None
        self.toy_name_edit = None
        self.age_edit = None

        # buttons to operate GUI
        self.add_into_table_btn = tk.Button(self.categories_master, text='Add Record to Categories Database',
                                            command=self.add)
        self.add_into_table_btn.grid(row=17, columnspan=5, pady=1, padx=5, ipadx=5)

        self.display_btn = tk.Button(self.categories_master, text='Display Records',
                                     command=self.display)
        self.display_btn.grid(row=15, columnspan=5, pady=1, padx=5, ipadx=5)

        self.delete_btn = tk.Button(self.categories_master, text='Delete Record',
                                    command=self.delete)
        self.delete_btn.grid(row=22, columnspan=5, pady=1, padx=5, ipadx=5)

        self.edit_btn = tk.Button(self.categories_master, text='Edit Record',
                                  command=self.edit)
        self.edit_btn.grid(row=23, columnspan=5, pady=1, padx=5, ipadx=5)

        self.exit_btn = tk.Button(self.categories_master, text='Exit',
                                  command=self.change_to_start)
        self.exit_btn.grid(row=25, columnspan=5, pady=1, padx=5, ipadx=5)

        self.remove_all_btn = tk.Button(self.categories_master, text='Clear Records',
                                        command=self.remove_all)
        self.remove_all_btn.grid(row=16, columnspan=5, pady=1, padx=5, ipadx=5)

        # open the table in treeview, add headings
        self.tree = ttk.Treeview(self.categories_master, column=("column1", "column2", "column3", "column4"),
                                 show='headings')
        self.tree.heading("#1", text="CATEGORY NAME")
        self.tree.heading("#2", text="TOY NAME")
        self.tree.heading("#3", text="AGE GROUP")
        self.tree.heading("#4", text="TOY ID")
        self.tree.grid(row=0, column=0, padx=50)

        # Create a table. Ignore if the table already exist in DB.

        self.cursor.execute("CREATE TABLE if not exists Categories ("
                            "Category_name TEXT, "
                            "Toy_name TEXT, "
                            "Age REAL"
                            ")")
        self.categories_master.pack()

    # instance method that will display popup window. It will be used in other instance methods.
    def empty(self):
        master_a = tk.Toplevel(self.categories_master)  # new window assign to categories frame
        master_a.title("Empty")  # '.title' is used to crete the title of our window
        master_a.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        master_a.configure(bg="azure3")  # This changes a color of our window
        tk.Label(master_a, bg="azure3", fg="black", text="Please enter ID").pack()  # This display a text.
        tk.Button(master_a, bg="white", fg="black", text="Back",
                  command=master_a.destroy).pack()  # Creates a button

    # This instance method will clear out the treeview table
    def remove_all(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

    # This instance method will add new category into DB. If category already exist it will display a notification.
    def add(self):
        # connect to a DB
        connect = sqlite3.connect('AllAboutToys.db')  # create/connect to db
        # cursor
        self.cursor = connect.cursor()
        # this code will
        self.cursor.execute("SELECT * FROM Categories WHERE category_name=:category_name AND"
                            " toy_name=:toy_name AND age=:age ",
                            {
                                'category_name': self.Category_name.get(),
                                'toy_name': self.Toy_name.get(),
                                'age': self.age.get(),
                            })

        # It will bring all records
        records = self.cursor.fetchall()

        if not records:
            self.cursor.execute("INSERT INTO Categories VALUES (:Category_name, :Toy_name, :age)",
                                {
                                    'Category_name': self.Category_name.get(),
                                    'Toy_name': self.Toy_name.get(),
                                    'age': self.age.get(),
                                })

            self.Category_name.delete(0, tk.END)
            self.Toy_name.delete(0, tk.END)
            self.age.delete(0, tk.END)
            # Commit changes
            connect.commit()
            # close connection
            connect.close()
        else:
            self.already_exist()  # popup window notification

    # instance method that will display popup window. It will be used in other instance methods.
    def already_exist(self):
        master2 = tk.Toplevel(self.categories_master)  # new window
        master2.title("Exist")  # '.title' is used to crete the title of our window
        master2.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        tk.Label(master2, bg="azure3", fg="black", text="Item already exist").pack()  # This display a text
        tk.Button(master2, bg="white", fg="black", text="Exit",
                  command=master2.destroy).pack()  # Creates a button
        master2.configure(bg="azure3")  # This changes a color of our window

    # this instance method will display all categories and put them inside the table.
    def display(self):
        self.connection = sqlite3.connect("AllAboutToys.db")  # connect to db
        cur = self.connection.cursor()
        cur.execute("SELECT *, oid FROM Categories")  # take all data from stock table
        rows = cur.fetchall()  # all data
        for row in rows:
            print(row)  # it print all records in the database
            self.tree.insert('', tk.END, values=row)  # insert in the treeview table
        self.connection.commit()  # commit changes
        self.connection.close()  # close connection

    # this instance method will take the category ID and delete it from the DB.
    def delete(self):
        connect = sqlite3.connect('AllAboutToys.db')  # create/connect to db
        # cursor
        self.cursor = connect.cursor()
        if entry := self.delete_window.get():  # check if value is in get and assign to entry box
            self.cursor.execute("DELETE from Categories WHERE oid = " + entry)
            self.delete_window.delete(0, tk.END)
            # Commit changes
            connect.commit()
        else:
            self.empty()
        # close connection
        connect.close()

    # this instance method will take the category ID find the category details and display them on the new popup window
    def edit(self):
        if entry := self.delete_window.get():  # check if value is in get and assign to entry box
            self.edit_master = tk.Toplevel(self.categories_master)  # new window
            self.edit_master.title('Update Records')  # name of the window
            self.edit_master.configure(bg='azure3')  # window colour
            self.edit_master.iconphoto(True,
                                       tk.PhotoImage(file="teddy-bear.png"))  # window icon
            # create/connect to db
            connect = sqlite3.connect('AllAboutToys.db')
            # cursor
            self.cursor = connect.cursor()
            self.cursor.execute("SELECT * FROM Categories WHERE oid = " + entry)
            # It will bring all records
            records = self.cursor.fetchall()
            # Entry boxes for our new window where data will be displayed and edited
            self.category_name_edit = tk.Entry(self.edit_master, width=30)
            self.category_name_edit.grid(row=0, column=1, padx=20, pady=(10, 0))

            self.toy_name_edit = tk.Entry(self.edit_master, width=30)
            self.toy_name_edit.grid(row=1, column=1)

            self.age_edit = tk.Entry(self.edit_master, width=30)
            self.age_edit.grid(row=2, column=1, padx=20)
            # Labels for my new window
            self.Category_name_label = tk.Label(self.edit_master, text='Category Name')
            self.Category_name_label.grid(row=0, column=0, pady=(10, 0))

            self.Toy_name_label = tk.Label(self.edit_master, text='Toy Name')
            self.Toy_name_label.grid(row=1, column=0)

            self.age_label = tk.Label(self.edit_master, text='Age group')
            self.age_label.grid(row=2, column=0)

            # loop through results and bring them into the entry boxes
            for record in records:
                self.category_name_edit.insert(0, record[0])
                self.toy_name_edit.insert(0, record[1])
                self.age_edit.insert(0, record[2])

            update_btn = tk.Button(self.edit_master, text='Update Record',
                                   command=self.update)  # button for update instance method
            update_btn.grid(row=4, columnspan=5, pady=1, padx=5, ipadx=5)
            # Commit changes
            connect.commit()
            # close connection
            connect.close()
        else:
            self.empty()  # popup window if user will not provide any ID

    # instance method to display popup window
    def msg_updated(self):
        master2 = tk.Toplevel(self.categories_master)  # new window
        master2.title("Data Updated")  # '.title' is used to crete the title of our window
        master2.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("Records Updated" + "\n " + "\n" + "%d/%m/%Y %H:%M:%S")
        tk.Label(master2, bg="azure3", fg="black", text=dt_string).pack()  # This display a text
        tk.Button(master2, bg="white", fg="black", text="Back",
                  command=master2.destroy).pack()  # Creates a button
        master2.configure(bg="azure3")  # This changes a color of our window

    # this instance methode will update the records that are edited inside edit() window
    def update(self):
        connect = sqlite3.connect('AllAboutToys.db')
        # cursor
        self.cursor = connect.cursor()
        records_id = self.delete_window.get()
        self.cursor.execute("""UPDATE Categories SET
                            Category_name =:Category,
                            Toy_name =:Toy,
                            age =:Age

                            WHERE oid =:oid""",
                            dict(Category=self.category_name_edit.get(), Toy=self.toy_name_edit.get(),
                                 Age=self.age_edit.get(), oid=records_id))

        # Commit changes
        connect.commit()
        # close connection
        connect.close()
        self.msg_updated()

        self.edit_master.destroy()  # close the window

    # this instance method will close the frame
    def change_to_start(self):
        self.categories_master.forget()


class Login(object):  # Class login
    def __init__(self):
        self.login_master = tk.Frame()  # instance attribute frame
        self.login_master.config(bg='azure3')  # background of a frame
        self.list_of_files = os.listdir()  # instance attribute that will create list
        self.user_credentials = None  # empty instance attribute that will store login and password details
        tk.Label(self.login_master, bg="azure3", fg="black", text="Please enter your details").pack()
        # text display
        self.username = tk.StringVar()  # this will hold the text variable username
        tk.Label(self.login_master, bg="azure3", fg="black",
                 text="Username ").pack()  # this will create text 'Username'
        self.username_entry = tk.Entry(self.login_master, textvariable=self.username)  # entry box
        self.username_entry.pack()
        self.password = tk.StringVar()  # this will hold the text variable password
        tk.Label(self.login_master, bg="azure3", fg="black",
                 text="Password").pack()  # this will create text 'Password'
        self.password_entry = tk.Entry(self.login_master, show='*', textvariable=self.password)  # entry window

        self.password_entry.pack()

    def login_authorisation(self):
        # this will take the input from entry windows
        self.user_credentials = self.username_entry.get() + " " + self.password_entry.get()
        # this method returns a list containing the names of the entries in the directory
        # given by path
        if "users.txt" in self.list_of_files:  # open file and read through lines
            file1 = open("users.txt", "r")
            users = file1.read().splitlines()
            if self.user_credentials in users:  # check if credentials are valid
                tk.Label(self.login_master, text="Login successful", bg="azure3", fg="black",
                         font=("arial", 11)).pack()
            else:
                self.password_invalid()  # that will display window with error

        self.password_entry.delete(0, tk.END)  # that will clear out our entry windows
        self.username_entry.delete(0, tk.END)

    def password_invalid(self):  # instance methode that will display an error message
        master_1 = tk.Toplevel(self.login_master)  # new window
        master_1.title("Invalid")  # '.title' is used to crete the title of our window
        master_1.geometry("250x100")  # '.geometry' is used to set the dimensions in Tkinter and set the position
        # of the main window
        tk.Label(master_1, bg="azure3", fg="black",
                 text="Invalid login or password").pack()  # This display a text. Also we can
        # change the color of our text
        # Creates a button
        tk.Button(master_1, bg="white", fg="black", text="OK", command=master_1.destroy).pack()
        master_1.configure(bg="azure3")  # This changes a color of our window


class RegisterScreen(Login):  # register class
    def __init__(self, master):  # here I assigned a new variable that is going to be used in this class function
        super().__init__()
        self.master = master
        self.register_master = tk.Frame()
        self.register_master.config(bg='azure3')

        tk.Label(self.register_master, bg="azure3", fg="black",
                 text="Please enter your details below").pack()  # Label for the screen
        tk.Label(self.register_master, bg="azure3", fg="black",
                 text="Username  ").pack()  # set of colors for Username window
        # self.username = tk.StringVar()  # This variable is getting an entry widget
        self.username_entry = tk.Entry(self.register_master,
                                       textvariable=self.username)  # This variable to enter a username
        self.username_entry.pack()  # This will implement the entry window
        # self.password = tk.StringVar()
        tk.Label(self.register_master, bg="azure3", fg="black",
                 text="Password  ").pack()  # set of colors for Password window
        self.password_entry = tk.Entry(self.register_master,
                                       textvariable=self.password)  # This variable to enter a password
        self.password_entry.pack()

        # Now I am creating the button to run register_user function

        tk.Button(self.register_master, bg="white", fg="black", text="Register", width=20, height=1,
                  command=self.register_user).pack(pady=1)

        tk.Button(self.register_master, bg="white", fg="black", text="Back to Login", width=20, height=1,
                  command=self.change_to_login).pack(pady=1)

        tk.Button(self.login_master, text="Login", bg="white", fg="black", width=10, height=1,
                  command=self.login_authorisation).pack(pady=1)  # button and the function that is assign to it

        tk.Button(self.login_master, bg="white", fg="black", text="GO to Register", width=20, height=1,
                  command=self.change_to_register).pack(pady=1)

        tk.Button(self.login_master, bg="white", fg="black", text="Exit", width=10, height=1,
                  command=self.change_to_start).pack(pady=1)

        self.login_master.pack()

    def change_to_login(self):
        self.login_master.pack(fill='both', expand=1)
        self.register_master.forget()

    def change_to_register(self):
        self.login_master.forget()
        self.register_master.pack(fill='both', expand=1)

    def change_to_start(self):
        self.login_master.forget()
        self.register_master.forget()

    def register_user(self):
        user_credentials = self.username_entry.get() + " " + self.password_entry.get()
        # this method returns a list containing the names of the entries in the directory
        # given by path
        if "users.txt" in self.list_of_files:  # This loop will check if the user already exist
            file1 = open("users.txt", "r")
            users = file1.read().splitlines()
            if user_credentials in users:
                tk.Label(self.register_master, text="User exist. You can login now.",
                         bg="azure3", fg="black", font=("arial", 11)).pack()  # that message will be displayed if
                # the user exist
                self.username_entry.delete(0, tk.END)  # this will clear entry window after user press a Register button
                self.password_entry.delete(0, tk.END)
                return

        file = open("users.txt", "a")  # This function opens/create the file and returns it as an object 'a' append
        file.write(self.username_entry.get() + " " + self.password_entry.get())
        file.write("\n")
        file.close()  # This function closes the open file
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        tk.Label(self.register_master, text="You just created an account", bg='azure3', fg="black",
                 font=("arial", 11)).pack()
        # this message will be displayed if we provide valid details


class MainScreen:  # class MainScreen will store all information about main screen and its features
    def __init__(self, master):  # our main window will be named master
        self.master = master
        self.master.title("AllAboutToys Ltd.")  # title main window
        self.master.configure(bg="azure3")  # background

        self.master.iconphoto(True,
                              tk.PhotoImage(file="teddy-bear.png"))  # this will add an teddy bear icon
        self.img = ImageTk.PhotoImage(Image.open("bear_bg_changed.jpg"))  # this will display the uploaded  image
        self.panel = tk.Label(self.master, bg='azure3', image=self.img)
        self.panel.pack(side="right", fill="both", expand="no")
        self.lbl_font = font.Font(family='Georgia',  # Font for our Label
                                  size='18',
                                  weight='bold')
        self.lbl_message = tk.Label(self.master,
                                    text='AllAboutToys: Administration Features',  # All details about message
                                    font=self.lbl_font,
                                    bg='azure3', fg='black')
        self.lbl_message.pack()  # this will add the label on the screen

        self.ac_mng_frame = tk.Frame()  # Here I created a Frames for each of my classes
        self.categories_frame = tk.Frame()
        self.products_frame = tk.Frame()
        self.stock_frame = tk.Frame()
        # The code below creates a buttons and classes assign to them
        self.but_ac_mng = tk.Button(self.ac_mng_frame, bg="white", fg="black", text="Account manager", width=20,
                                    height=1,
                                    command=lambda: RegisterScreen(self.ac_mng_frame)).pack()

        self.but_categories = tk.Button(self.categories_frame, bg="white", fg="black", text="Categories", width=20,
                                        height=1,
                                        command=lambda: Categories(self.categories_frame)).pack()

        self.but_prod = tk.Button(self.products_frame, bg="white", fg="black", text="Products", width=20,
                                  height=1,
                                  command=lambda: Products(self.products_frame)).pack()

        self.but_stock = tk.Button(self.stock_frame, bg="white", fg="black", text="Stock",
                                   width=20,
                                   height=1,
                                   command=lambda: Stock(self.stock_frame)).pack()

        self.ac_mng_frame.pack()  # here I allocate the buttons on the screen
        self.categories_frame.pack()
        self.products_frame.pack()
        self.stock_frame.pack()

        def center_window_on_screen():  # this function will display main window in the center of the computer
            # screen
            x_cord = int((screen_width / 2) - (width / 2))
            y_cord = int((screen_height / 2) - (height / 2))
            root.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))

        width, height = 1000, 1000
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_window_on_screen()


root = tk.Tk()  # we are creating variable with tk.Tk()
my_gui = MainScreen(root)  # we are calling main screen class
root.mainloop()  # run main loop
