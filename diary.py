import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector

class DiaryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Diary Manager")
        self.root.geometry("1540x840")

        # Main Frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Title
        ctk.CTkLabel(main_frame, text="Diary Manager", text_color="#1F538D", font=("Arial Black", 20)).place(x=170, y=25)

        # Left Frame for Entry Details
        details_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        details_frame.grid(row=0, column=0, padx=20, pady=70, sticky="ne")

        # Date and Record Entry Fields
        ctk.CTkLabel(details_frame, text="Entry Date:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_date = DateEntry(details_frame, width=17, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_date.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(details_frame, text="Record:").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.record_entry = ctk.CTkTextbox(details_frame, width=300, height=580,fg_color="white",text_color="black")
        self.record_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        self.save_button = ctk.CTkButton(details_frame, text="Save", command=self.save_entry)
        self.save_button.grid(row=2, column=0, padx=10, pady=10)

        self.update_button = ctk.CTkButton(details_frame, text="Update", command=self.update_entry)
        self.update_button.grid(row=2, column=1, padx=10, pady=10)

        self.delete_button = ctk.CTkButton(details_frame, text="Delete", command=self.delete_entry)
        self.delete_button.grid(row=3, column=0, padx=10, pady=10)

        self.reset_button = ctk.CTkButton(details_frame, text="Reset", command=self.reset_form)
        self.reset_button.grid(row=3, column=1, padx=10, pady=10)

        # Treeview for Displaying Entries
        columns = ("entry_date", "record")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=42)
        self.tree.place(x=650, y=50)

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150 if col == "entry_date" else 1100, anchor="w")
        
   
            

        self.display_entries()
        self.tree.bind("<ButtonRelease-1>", self.get_selected_row)

        # Search Frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.place(x=750, y=750)

        # Search Attribute Dropdown and Search Entry
        self.search_attr_var = ctk.StringVar(value="Select Attribute")
        attributes = ["Entry Date", "Record"]
        self.attribute_menu = ctk.CTkOptionMenu(button_frame, variable=self.search_attr_var, values=attributes, width=150)
        self.attribute_menu.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(button_frame, width=150)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ctk.CTkButton(button_frame, text="Search", fg_color="green", width=100, command=self.search_diary)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.show_all_button = ctk.CTkButton(button_frame, text="Show All", fg_color="green", width=100, command=self.display_entries)
        self.show_all_button.grid(row=0, column=3, padx=10, pady=10)

    def search_diary(self):
        # Get the selected attribute and search value
        attribute = self.search_attr_var.get()
        search_value = self.search_entry.get().strip()

        if attribute == "Select Attribute" or not search_value:
            messagebox.showwarning("Input Error", "Please select an attribute and enter a value to search.")
            return

        # Mapping the attribute to column names in the database
        column_map = {
            "Entry Date": "entry_date",
            "Record": "record"
        }

        # Get the actual column name for SQL query
        column = column_map.get(attribute)

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()

            # Perform the search query using LIKE for partial matches
            query = f"SELECT * FROM diary WHERE {column} LIKE %s"
            cursor.execute(query, (f"%{search_value}%",))
            rows = cursor.fetchall()
            connection.close()

            # Clear previous results
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert filtered results into the Treeview
            for row in rows:
                self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def display_entries(self):
        # Clear Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Connect to the MySQL database and fetch entries
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kbot",
            database="hotel_management",
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM diary;")
        rows = cursor.fetchall()
        connection.close()

        # Insert entries into the Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def get_selected_row(self, event):
        # Get selected item from the Treeview
        selected_item = self.tree.selection()
        if selected_item:
            # Extract the values from the selected item
            item = self.tree.item(selected_item)
            entry_date, record = item["values"]

            # Set the values in the entry fields
            self.entry_date.set_date(entry_date)
            self.record_entry.delete("1.0", 'end')
            self.record_entry.insert('end', record)

    def save_entry(self):
        entry_date = self.entry_date.get()
        record = self.record_entry.get("1.0", 'end').strip()

        if not record:
            messagebox.showwarning("Input Error", "Please enter a record.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO diary (entry_date, record) VALUES (%s, %s)", (entry_date, record))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Diary entry saved successfully!")
            self.reset_form()  # Reset the form after save
            self.display_entries()  # Refresh the table after save

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def update_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an entry to update.")
            return

        entry_date = self.entry_date.get()
        record = self.record_entry.get("1.0", 'end').strip()

        if not record:
            messagebox.showwarning("Input Error", "Please enter a record.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()
            cursor.execute("UPDATE diary SET record = %s WHERE entry_date = %s", (record, entry_date))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Diary entry updated successfully!")
            self.reset_form()  # Reset the form after update
            self.display_entries()  # Refresh the table after update

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        self.display_entries()  # Refresh the table after update

    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an entry to delete.")
            return

        entry_date = self.entry_date.get()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM diary WHERE entry_date = %s", (entry_date,))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Diary entry deleted successfully!")
            self.reset_form()  # Reset the form after delete
            self.display_entries()  # Refresh the table after delete

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def reset_form(self):
        # Clear all input fields
        for entry in self.entries.values():
            if isinstance(entry, ctk.CTkOptionMenu):
                entry.set("Select")  # Reset dropdown menus
            else:
                entry.delete(0, 'end')  

if __name__ == "__main__":
    root = ctk.CTk()
    app = DiaryManager(root)
    root.mainloop()
