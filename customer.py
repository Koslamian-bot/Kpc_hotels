import customtkinter as ctk  # Use customtkinter for UI
import mysql.connector
from tkinter import messagebox
from tkinter import ttk  # For using Treeview
from tkcalendar import DateEntry  # Import DateEntry for date picking

class CusInfo:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Info")
        self.root.geometry("1540x840")

        # Create a frame with customtkinter
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Left frame for customer details
        details_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        details_frame.grid(row=0, column=0, padx=20, pady=70, sticky="ne")

        ctk.CTkLabel(main_frame, text="Add a new customer", text_color="#1F538D", font=("Arial Black", 20)).place(x=170, y=25)

        # Right frame for search and options buttons
        button_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        button_frame.grid(row=2, column=1, padx=170, pady=20, sticky="s")

        # Add customer detail labels and entry fields
        labels = ["Customer Name", "Phone Number", "Email ID", "Address", "Date of Birth", "Gender", "Nationality", "ID Proof", "ID Number"]
        self.entries = {}

        # Dropdowns for Gender, Nationality, and ID Proof
        self.gender_var = ctk.StringVar()
        self.nationality_var = ctk.StringVar()
        self.id_proof_var = ctk.StringVar()

        for i, label in enumerate(labels):
            ctk.CTkLabel(details_frame, text=f"{label}:").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            if label == "Gender":
                self.entries[label] = ctk.CTkOptionMenu(details_frame, variable=self.gender_var, values=["Male", "Female", "Other"])
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            elif label == "Nationality":
                countries = ["Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Timor-Leste", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"]  # Example country list
                self.entries[label] = ctk.CTkOptionMenu(details_frame, variable=self.nationality_var, values=countries)
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            elif label == "ID Proof":
                self.entries[label] = ctk.CTkOptionMenu(details_frame, variable=self.id_proof_var, values=["Passport", "National ID", "Driving License"])
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            elif label == "Date of Birth":
                self.entries[label] = DateEntry(details_frame, width=18, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")  # Date picker
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            else:
                entry = ctk.CTkEntry(details_frame, width=300)
                entry.grid(row=i, column=1, padx=10, pady=10)
                self.entries[label] = entry

        # Action buttons below the form (Save, Update, Delete, Reset)
        self.save_button = ctk.CTkButton(details_frame, text="Save", command=self.save_customer)
        self.save_button.grid(row=9, column=0, padx=10, pady=10)

        self.update_button = ctk.CTkButton(details_frame, text="Update", command=self.update_customer)
        self.update_button.grid(row=9, column=1, padx=10, pady=10)

        self.delete_button = ctk.CTkButton(details_frame, text="Delete", command=self.delete_customer)
        self.delete_button.grid(row=10, column=0, padx=10, pady=10)

        self.reset_button = ctk.CTkButton(details_frame, text="Reset", command=self.reset_form)
        self.reset_button.grid(row=10, column=1, padx=10, pady=10)

        # Dropdown for selecting attribute and text box for input
        self.search_attr_var = ctk.StringVar(value="Select Attribute")
        attributes = ["customer_id", "customer_name", "phone", "email", "address", "DOB", "gender", "nationality", "id_proof", "id_number"]
        self.attribute_menu = ctk.CTkOptionMenu(button_frame, variable=self.search_attr_var, values=attributes, width=150)
        self.attribute_menu.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(button_frame, width=150)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ctk.CTkButton(button_frame, text="Search", fg_color="green", width=100, command=self.search_customer)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.show_all_button = ctk.CTkButton(button_frame, text="Show All", fg_color="green", width=100, command=self.display_customers)
        self.show_all_button.grid(row=0, column=3, padx=10, pady=10)

        # Treeview table for displaying customers
        columns = ("customer_id", "customer_name", "phone", "email", "address", "DOB", "gender", "nationality", "id_proof", "id_number")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=35)
        self.tree.place(x=250, y=200)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.bind("<ButtonRelease-1>", self.populate_form)  # Bind selection to form population

        self.tree.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="ne")

        # Call method to display customers
        self.display_customers()
    def display_customers(self):
        # Clear the Treeview before populating
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kbot",
            database="hotel_management",
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers;")  # Query the customers table

        # Fetch all rows from the database
        rows = cursor.fetchall()
        connection.close()

        # Insert data into the Treeview widget
        for row in rows:
            self.tree.insert("", "end", values=row)

    def populate_form(self, event):
        """Populates the form with selected customer's data from Treeview."""
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            # Set entries with selected customer data
            self.entries["Customer Name"].delete(0, "end")
            self.entries["Customer Name"].insert(0, item_values[1])

            self.entries["Phone Number"].delete(0, "end")
            self.entries["Phone Number"].insert(0, item_values[2])

            self.entries["Email ID"].delete(0, "end")
            self.entries["Email ID"].insert(0, item_values[3])

            self.entries["Address"].delete(0, "end")
            self.entries["Address"].insert(0, item_values[4])

            self.entries["Date of Birth"].delete(0, "end")
            self.entries["Date of Birth"].insert(0, item_values[5])

            self.gender_var.set(item_values[6])
            self.nationality_var.set(item_values[7])
            self.id_proof_var.set(item_values[8])

            self.entries["ID Number"].delete(0, "end")
            self.entries["ID Number"].insert(0, item_values[9])

    def update_customer(self):
        # Get selected item from Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a customer to update.")
            return

        customer_id = self.tree.item(selected_item)["values"][0]

        # Get updated data from input fields
        customer_name = self.entries["Customer Name"].get()
        phone = self.entries["Phone Number"].get()
        email = self.entries["Email ID"].get()
        address = self.entries["Address"].get()
        dob = self.entries["Date of Birth"].get()
        gender = self.gender_var.get()
        nationality = self.nationality_var.get()
        id_proof = self.id_proof_var.get()
        id_number = self.entries["ID Number"].get()

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()

            update_query = """
            UPDATE customers 
            SET customer_name=%s, phone=%s, email=%s, address=%s, DOB=%s, gender=%s, nationality=%s, id_proof=%s, id_number=%s 
            WHERE customer_id=%s
            """
            cursor.execute(update_query, (customer_name, phone, email, address, dob, gender, nationality, id_proof, id_number, customer_id))

            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Customer information updated successfully.")
            self.display_customers()  # Refresh the customer table

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating customer: {err}")

    def save_customer(self):
        """Inserts new customer details into the database"""
        customer_name = self.entries["Customer Name"].get()
        phone = self.entries["Phone Number"].get()
        email = self.entries["Email ID"].get()
        address = self.entries["Address"].get()
        dob = self.entries["Date of Birth"].get()
        gender = self.gender_var.get()
        nationality = self.nationality_var.get()
        id_proof = self.id_proof_var.get()
        id_number = self.entries["ID Number"].get()

        # Validate inputs
        if not customer_name or not phone or not email:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()

            # Insert new customer into the customers table
            insert_query = """
            INSERT INTO customers (customer_name, phone, email, address, DOB, gender, nationality, id_proof, id_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (customer_name, phone, email, address, dob, gender, nationality, id_proof, id_number))

            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "New customer added successfully.")
            self.display_customers()  # Refresh the customer table

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting customer: {err}")

    def delete_customer(self):
        """Deletes the selected customer from the database"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a customer to delete.")
            return

        customer_id = self.tree.item(selected_item)["values"][0]
        confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this customer?")
        if confirmation:
            try:
                # Connect to the MySQL database
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="kbot",
                    database="hotel_management",
                )
                cursor = connection.cursor()

                delete_query = "DELETE FROM customers WHERE customer_id=%s"
                cursor.execute(delete_query, (customer_id,))

                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Customer deleted successfully.")
                self.display_customers()  # Refresh the customer table

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting customer: {err}")

    def reset_form(self):
        # Clear all input fields
        for entry in self.entries.values():
            if isinstance(entry, ctk.CTkOptionMenu):
                entry.set("Select")  # Reset dropdown menus
            else:
                entry.delete(0, 'end')  # Clear text fields

    def search_customer(self):
        """Searches for a customer by the selected attribute and search term"""
        search_attr = self.search_attr_var.get()
        search_term = self.search_entry.get()

        if search_attr == "Select Attribute" or not search_term:
            messagebox.showwarning("Search Error", "Please select an attribute and enter a search term.")
            return

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()

            # Perform the search query
            search_query = f"SELECT * FROM customers WHERE {search_attr} LIKE %s"
            cursor.execute(search_query, (f"%{search_term}%",))

            rows = cursor.fetchall()
            connection.close()

            # Clear the Treeview before inserting search results
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert search results into the Treeview widget
            for row in rows:
                self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error searching customer: {err}")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: "light", "dark", "system"
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"
    root = ctk.CTk()
    app = CusInfo(root)
    root.mainloop()