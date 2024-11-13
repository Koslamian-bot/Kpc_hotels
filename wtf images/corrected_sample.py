from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class Cust_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer")
        self.root.geometry("1121x452+234+243")

        # Variables
        self.var_cust_name = StringVar()
        self.var_phone = StringVar()
        self.var_email = StringVar()
        self.var_address = StringVar()
        self.var_dob = StringVar()
        self.var_gender = StringVar()
        self.var_nationality = StringVar()
        self.var_id_proof = StringVar()
        self.var_id_number = StringVar()

        # Title
        lbl_title = Label(self.root, text="CUSTOMER DETAILS", font=("times new roman", 18, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1121, height=35)

        # Label Frame for form inputs
        lblFrameLeft = LabelFrame(self.root, bd=2, relief=RIDGE, text="CUSTOMER DETAILS", font=("times new roman", 12, "bold"), padx=2)
        lblFrameLeft.place(x=5, y=40, width=425, height=410)

        # Form labels and entry fields

        # Customer Name
        lbl_cust_name = Label(lblFrameLeft, text="CUSTOMER NAME:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_cust_name.grid(row=0, column=0, sticky=W)
        entry_name = ttk.Entry(lblFrameLeft, textvariable=self.var_cust_name, width=29, font=("arial", 11, "bold"))
        entry_name.grid(row=0, column=1)

        # Phone
        lbl_phone = Label(lblFrameLeft, text="PHONE:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_phone.grid(row=1, column=0, sticky=W)
        entry_phone = ttk.Entry(lblFrameLeft, textvariable=self.var_phone, width=29, font=("arial", 11, "bold"))
        entry_phone.grid(row=1, column=1)

        # Email
        lbl_email = Label(lblFrameLeft, text="EMAIL:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_email.grid(row=2, column=0, sticky=W)
        entry_email = ttk.Entry(lblFrameLeft, textvariable=self.var_email, width=29, font=("arial", 11, "bold"))
        entry_email.grid(row=2, column=1)

        # Address
        lbl_address = Label(lblFrameLeft, text="ADDRESS:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_address.grid(row=3, column=0, sticky=W)
        entry_address = ttk.Entry(lblFrameLeft, textvariable=self.var_address, width=29, font=("arial", 11, "bold"))
        entry_address.grid(row=3, column=1)

        # DOB
        lbl_dob = Label(lblFrameLeft, text="DOB:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_dob.grid(row=4, column=0, sticky=W)
        entry_dob = ttk.Entry(lblFrameLeft, textvariable=self.var_dob, width=29, font=("arial", 11, "bold"))
        entry_dob.grid(row=4, column=1)

        # Gender
        lbl_gender = Label(lblFrameLeft, text="GENDER:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_gender.grid(row=5, column=0, sticky=W)
        combo_gender = ttk.Combobox(lblFrameLeft, textvariable=self.var_gender, font=("arial", 10, "bold"), width=31, state="readonly")
        combo_gender["value"] = ("MALE", "FEMALE", "OTHERS")
        combo_gender.current(0)
        combo_gender.grid(row=5, column=1)

        # Nationality
        lbl_nationality = Label(lblFrameLeft, text="NATIONALITY:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_nationality.grid(row=6, column=0, sticky=W)
        combo_nationality = ttk.Combobox(lblFrameLeft, textvariable=self.var_nationality, font=("arial", 10, "bold"), width=31, state="readonly")
        combo_nationality["value"] = ("AMERICAN", "BRITISH", "INDIAN")
        combo_nationality.current(0)
        combo_nationality.grid(row=6, column=1)

        # ID Proof Type
        lbl_id_proof = Label(lblFrameLeft, text="ID PROOF TYPE:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_id_proof.grid(row=7, column=0, sticky=W)
        combo_id_proof = ttk.Combobox(lblFrameLeft, textvariable=self.var_id_proof, font=("arial", 10, "bold"), width=31, state="readonly")
        combo_id_proof["value"] = ("AADHAR CARD", "PASSPORT", "DRIVING LICENSE", "PAN CARD")
        combo_id_proof.current(0)
        combo_id_proof.grid(row=7, column=1)

        # ID Number
        lbl_id_number = Label(lblFrameLeft, text="ID NUMBER:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_id_number.grid(row=8, column=0, sticky=W)
        entry_id_number = ttk.Entry(lblFrameLeft, textvariable=self.var_id_number, width=29, font=("arial", 11, "bold"))
        entry_id_number.grid(row=8, column=1)

        # Buttons for CRUD operations
        btn_frame = Label(lblFrameLeft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=352, width=412, height=32)

        btn_add = Button(btn_frame, text="ADD", command=self.add_data, font=("arial", 10, "bold"), bg="black", fg="gold", width=10)
        btn_add.grid(row=0, column=0, padx=5)

        btn_update = Button(btn_frame, text="UPDATE", command=self.update, font=("arial", 10, "bold"), bg="black", fg="gold", width=10)
        btn_update.grid(row=0, column=1, padx=5)

        btn_delete = Button(btn_frame, text="DELETE", command=self.dat_Delete, font=("arial", 10, "bold"), bg="black", fg="gold", width=10)
        btn_delete.grid(row=0, column=2, padx=5)

        btn_reset = Button(btn_frame, text="RESET", command=self.data_reset, font=("arial", 10, "bold"), bg="black", fg="gold", width=10)
        btn_reset.grid(row=0, column=3, padx=5)

        # Table Frame for search and display
        table_frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="SEARCH AND VIEW DETAILS", font=("times new roman", 12, "bold"), padx=2)
        table_frame.place(x=435, y=40, width=680, height=410)

        lblsearchby = Label(table_frame, text="SEARCH BY:", font=("arial", 10, "bold"), bg="red", fg="white")
        lblsearchby.grid(row=0, column=0, sticky=W, padx=4)

        self.search_var = StringVar()
        combo_search = ttk.Combobox(table_frame, textvariable=self.search_var, font=("arial", 10, "bold"), width=12, state="readonly")
        combo_search["value"] = ("phone", "customer_name")
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=4)

        self.txt_search = StringVar()
        entry_search = ttk.Entry(table_frame, textvariable=self.txt_search, width=29, font=("arial", 11, "bold"))
        entry_search.grid(row=0, column=2, padx=4)

        btn_search = Button(table_frame, text="SEARCH", command=self.search_data, font=("arial", 10, "bold"), bg="black", fg="gold", width=10)
        btn_search.grid(row=0, column=3, padx=5)

        btn_showall = Button(table_frame, text="SHOW ALL!!", command=self.fetch_data, font=("arial", 10, "bold"), bg="black", fg="gold", width=10)
        btn_showall.grid(row=0, column=4, padx=5)

        # Show data table
        details_table = Label(table_frame, bd=2, relief=RIDGE)
        details_table.place(x=0, y=34, width=674, height=350)

        Scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.Cust_details_table = ttk.Treeview(details_table, columns=("customer_id", "customer_name", "phone", "email", "address", "DOB", "gender", "nationality", "id_proof", "id_number"), xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)
        Scroll_x.pack(side=BOTTOM, fill=X)
        Scroll_y.pack(side=RIGHT, fill=Y)

        Scroll_x.config(command=self.Cust_details_table.xview)
        Scroll_y.config(command=self.Cust_details_table.yview)

        self.Cust_details_table.heading("customer_id", text="ID")
        self.Cust_details_table.heading("customer_name", text="NAME")
        self.Cust_details_table.heading("phone", text="PHONE")
        self.Cust_details_table.heading("email", text="EMAIL")
        self.Cust_details_table.heading("address", text="ADDRESS")
        self.Cust_details_table.heading("DOB", text="DOB")
        self.Cust_details_table.heading("gender", text="GENDER")
        self.Cust_details_table.heading("nationality", text="NATIONALITY")
        self.Cust_details_table.heading("id_proof", text="ID PROOF")
        self.Cust_details_table.heading("id_number", text="ID NO.")

        self.Cust_details_table["show"] = "headings"

        self.Cust_details_table.column("customer_id", width=100)
        self.Cust_details_table.column("customer_name", width=100)
        self.Cust_details_table.column("phone", width=100)
        self.Cust_details_table.column("email", width=100)
        self.Cust_details_table.column("address", width=100)
        self.Cust_details_table.column("DOB", width=100)
        self.Cust_details_table.column("gender", width=100)
        self.Cust_details_table.column("nationality", width=100)
        self.Cust_details_table.column("id_proof", width=100)
        self.Cust_details_table.column("id_number", width=100)

        self.Cust_details_table.pack(fill=BOTH, expand=1)
        self.Cust_details_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

    def add_data(self):
        if self.var_cust_name.get() == "" or self.var_phone.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="Electrabuzz2006", database="hms")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into customers (customer_name, phone, email, address, DOB, gender, nationality, id_proof, id_number) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    self.var_cust_name.get(),
                    self.var_phone.get(),
                    self.var_email.get(),
                    self.var_address.get(),
                    self.var_dob.get(),
                    self.var_gender.get(),
                    self.var_nationality.get(),
                    self.var_id_proof.get(),
                    self.var_id_number.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Customer has been added", parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="Electrabuzz2006", database="hms")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from customers")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.Cust_details_table.delete(*self.Cust_details_table.get_children())
            for i in rows:
                self.Cust_details_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.Cust_details_table.focus()
        content = self.Cust_details_table.item(cursor_row)
        row = content["values"]

        self.var_cust_name.set(row[1])
        self.var_phone.set(row[2])
        self.var_email.set(row[3])
        self.var_address.set(row[4])
        self.var_dob.set(row[5])
        self.var_gender.set(row[6])
        self.var_nationality.set(row[7])
        self.var_id_proof.set(row[8])
        self.var_id_number.set(row[9])

    def update(self):
        if self.var_phone.get() == "":
            messagebox.showerror("Error", "Please enter phone number", parent=self.root)
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="Electrabuzz2006", database="hms")
            my_cursor = conn.cursor()
            my_cursor.execute("update customers set customer_name=%s, phone=%s, email=%s, address=%s, DOB=%s, gender=%s, nationality=%s, id_proof=%s, id_number=%s where customer_id=%s", (
                self.var_cust_name.get(),
                self.var_phone.get(),
                self.var_email.get(),
                self.var_address.get(),
                self.var_dob.get(),
                self.var_gender.get(),
                self.var_nationality.get(),
                self.var_id_proof.get(),
                self.var_id_number.get(),
                self.Cust_details_table.item(self.Cust_details_table.focus())["values"][0]  # customer_id
            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Update", "Customer details have been updated", parent=self.root)

    def dat_Delete(self):
        delete_confirm = messagebox.askyesno("Hotel Management System", "Do you want to delete this customer?", parent=self.root)
        if delete_confirm:
            conn = mysql.connector.connect(host="localhost", username="root", password="Electrabuzz2006", database="hms")
            my_cursor = conn.cursor()
            query = "delete from customers where customer_id=%s"
            value = (self.Cust_details_table.item(self.Cust_details_table.focus())["values"][0],)
            my_cursor.execute(query, value)
            conn.commit()
            self.fetch_data()
            conn.close()

    def data_reset(self):
        self.var_cust_name.set("")
        self.var_phone.set("")
        self.var_email.set("")
        self.var_address.set("")
        self.var_dob.set("")
        self.var_gender.set("")
        self.var_nationality.set("")
        self.var_id_proof.set("")
        self.var_id_number.set("")

    def search_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="Electrabuzz2006", database="hms")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from customers where " + str(self.search_var.get()) + " LIKE '%" + str(self.txt_search.get()) + "%'")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.Cust_details_table.delete(*self.Cust_details_table.get_children())
            for i in rows:
                self.Cust_details_table.insert("", END, values=i)
            conn.commit()
        conn.close()

if __name__ == "__main__":
    root = Tk()
    
# Ensuring root is initialized
root = Tk()
obj = Cust_Win(root)
root.mainloop()

    root.mainloop()
