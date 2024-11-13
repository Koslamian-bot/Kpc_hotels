import customtkinter as ctk  # Use customtkinter for UI 
import mysql.connector
from tkinter import messagebox
from tkinter import ttk  # For using Treeview
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

class StaffInfo:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff Info")
        self.root.geometry("1540x840")

        # Create a frame with customtkinter
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Left frame for staff details
        details_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        details_frame.grid(row=0, column=0, padx=20, pady=70, sticky="ne")

        ctk.CTkLabel(main_frame, text="Add a new staff member", text_color="#1F538D", font=("Arial Black", 20)).place(x=170, y=25)

        # Right frame for search and options buttons
        button_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        button_frame.grid(row=2, column=1, padx=170, pady=20, sticky="s")

        # Add staff detail labels and entry fields
        labels = ["Staff Name", "Gender", "Nationality", "Designation", "Phone Number", "Work Experience", "Hire Date", "Salary", "Shift Timings"]
        self.entries = {}

        # Dropdowns for Gender, Nationality, and Designation
        self.gender_var = ctk.StringVar()
        self.nationality_var = ctk.StringVar()
        self.designation_var = ctk.StringVar()
        self.st_var=ctk.StringVar()

        for i, label in enumerate(labels):
            ctk.CTkLabel(details_frame, text=f"{label}:").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            if label == "Gender":
                self.entries[label] = ctk.CTkOptionMenu(details_frame, variable=self.gender_var, values=["Male", "Female", "Other"])
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            elif label == "Nationality":
                countries = ["Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Timor-Leste", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"]  # Add more as needed
                self.entries[label] = ctk.CTkOptionMenu(details_frame, variable=self.nationality_var, values=countries)
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            elif label == "Designation":
                self.entries[label] = ctk.CTkOptionMenu(details_frame, variable=self.designation_var, values=["RoomService", "Receptionist", "Manager", "Chef", "Waiters", "Drivers","Accountant"])
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            elif label == "Hire Date":
                # Use DateEntry from tkcalendar for date selection
                self.entries[label] = DateEntry(details_frame, width=17, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)
            elif label == "Shift Timings":
                self.entries[label] = ctk.CTkOptionMenu(details_frame, variable=self.st_var, values=["9:00 AM - 5:00 PM", "10:00 AM - 6:00 PM", "11:00 AM - 7:00 PM", "2:00 PM - 10:00 PM", "6:00 PM - 2:00 AM"])
                self.entries[label].grid(row=i, column=1, padx=10, pady=10)    
            else:
                entry = ctk.CTkEntry(details_frame, width=300)
                entry.grid(row=i, column=1, padx=10, pady=10)
                self.entries[label] = entry

        # Action buttons below the form (Save, Update, Delete, Reset)
        self.save_button = ctk.CTkButton(details_frame, text="Save", command=self.save_staff)
        self.save_button.grid(row=9, column=0, padx=10, pady=10)

        self.update_button = ctk.CTkButton(details_frame, text="Update", command=self.update_staff)
        self.update_button.grid(row=9, column=1, padx=10, pady=10)

        self.delete_button = ctk.CTkButton(details_frame, text="Delete", command=self.delete_staff)
        self.delete_button.grid(row=10, column=0, padx=10, pady=10)

        self.reset_button = ctk.CTkButton(details_frame, text="Reset", command=self.reset_form)
        self.reset_button.grid(row=10, column=1, padx=10, pady=10)

        # Dropdown for selecting attribute and text box for input
        self.search_attr_var = ctk.StringVar(value="Select Attribute")
        attributes = ["Staff_id", "Staff_name", "Gender", "Staff_nationality", "Staff_Designation", "Staffphone_no", "Work_experience", "Hire_date", "Salary", "Shift_timings"]
        self.attribute_menu = ctk.CTkOptionMenu(button_frame, variable=self.search_attr_var, values=attributes, width=150)
        self.attribute_menu.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(button_frame, width=150)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ctk.CTkButton(button_frame, text="Search", fg_color="green", width=100, command=self.search_staff)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.show_all_button = ctk.CTkButton(button_frame, text="Show All", fg_color="green", width=100, command=self.display_staff)
        self.show_all_button.grid(row=0, column=3, padx=10, pady=10)

        # Treeview table for displaying staff
        columns = ("Staff_id", "Staff_name", "Gender", "Staff_nationality", "Staff_Designation", "Staffphone_no", "Work_experience", "Hire_date", "Salary", "Shift_timings")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=35)
        self.tree.place(x=250, y=200)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="ne")

        # Call method to display staff
        self.display_staff()
        self.tree.bind("<ButtonRelease-1>", self.get_selected_row)

    def get_selected_row(self, event):
        selected_item = self.tree.selection()  # Get the selected item in Treeview
        if not selected_item:
            return

        # Get the data from the selected row
        row_values = self.tree.item(selected_item, "values")

        # Populate the input fields with the corresponding data
        self.entries["Staff Name"].delete(0, 'end')
        self.entries["Staff Name"].insert(0, row_values[1])

        self.gender_var.set(row_values[2])  # Assuming gender is at index 2

        self.nationality_var.set(row_values[3])  # Assuming nationality is at index 3

        self.designation_var.set(row_values[4])  # Assuming designation is at index 4

        self.entries["Phone Number"].delete(0, 'end')
        self.entries["Phone Number"].insert(0, row_values[5])

        self.entries["Work Experience"].delete(0, 'end')
        self.entries["Work Experience"].insert(0, row_values[6])

        self.entries["Hire Date"].set_date(row_values[7])  # Use set_date for DateEntry

        self.entries["Salary"].delete(0, 'end')
        self.entries["Salary"].insert(0, row_values[8])

        self.entries["Shift Timings"].delete(0, 'end')
        self.entries["Shift Timings"].insert(0, row_values[9])

    def get_selected_row(self, event):
        selected_item = self.tree.selection()  # Get the selected item in Treeview
        if not selected_item:
            return

        # Get the data from the selected row
        row_values = self.tree.item(selected_item, "values")

        # Populate the input fields with the corresponding data
        self.entries["Staff Name"].delete(0, 'end')
        self.entries["Staff Name"].insert(0, row_values[1])

        self.gender_var.set(row_values[2])  # Assuming gender is at index 2

        self.nationality_var.set(row_values[3])  # Assuming nationality is at index 3

        self.designation_var.set(row_values[4])  # Assuming designation is at index 4

        self.entries["Phone Number"].delete(0, 'end')
        self.entries["Phone Number"].insert(0, row_values[5])

        self.entries["Work Experience"].delete(0, 'end')
        self.entries["Work Experience"].insert(0, row_values[6])

        self.entries["Hire Date"].delete(0, 'end')
        self.entries["Hire Date"].insert(0, row_values[7])

        self.entries["Salary"].delete(0, 'end')
        self.entries["Salary"].insert(0, row_values[8])

        self.entries["Shift Timings"].delete(0, 'end')
        self.entries["Shift Timings"].insert(0, row_values[9])

    def display_staff(self):
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
        cursor.execute("SELECT * FROM staff;")  # Query the staff table

        # Fetch all rows from the database
        rows = cursor.fetchall()
        connection.close()

        # Insert data into the Treeview widget
        for row in rows:
            self.tree.insert("", "end", values=row)

    def search_staff(self):
        # Get the selected attribute and input value
        attribute = self.search_attr_var.get()
        search_value = self.search_entry.get()

        if not attribute or not search_value:
            messagebox.showwarning("Input Error", "Please select an attribute and enter a value to search.")
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
            query = f"SELECT * FROM staff WHERE {attribute} = %s"
            cursor.execute(query, (search_value,))
            rows = cursor.fetchall()
            connection.close()

            # Clear previous results
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert new results
            for row in rows:
                self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def save_staff(self):
        # Get data from input fields
        staff_name = self.entries["Staff Name"].get()
        gender = self.gender_var.get()
        nationality = self.nationality_var.get()
        designation = self.designation_var.get()
        phone = self.entries["Phone Number"].get()
        work_experience = self.entries["Work Experience"].get()
        hire_date = self.entries["Hire Date"].get()
        salary = self.entries["Salary"].get()
        shift_timings = self.entries["Shift Timings"].get()

        # Check if mandatory fields are filled
        if not staff_name or not designation or not phone:
            messagebox.showwarning("Input Error", "Please fill in all required fields (Name, Designation, Phone Number).")
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

            # Insert staff details into the database
            cursor.execute(
                "INSERT INTO staff (Staff_name, Gender, Staff_nationality, Staff_Designation, Staffphone_no, Work_experience, Hire_date, Salary, Shift_timings) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (staff_name, gender, nationality, designation, phone, work_experience, hire_date, salary, shift_timings)
            )
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Staff details saved successfully!")
            self.reset_form()
            self.display_staff()  # Refresh the table after saving

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def update_staff(self):
        # Get selected item from Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a staff member to update.")
            return

        # Get the staff ID of the selected row (assuming the first column is the staff_id)
        staff_id = self.tree.item(selected_item)["values"][0]

        # Get updated data from input fields
        staff_name = self.entries["Staff Name"].get()
        gender = self.gender_var.get()
        nationality = self.nationality_var.get()
        designation = self.designation_var.get()
        phone = self.entries["Phone Number"].get()
        work_experience = self.entries["Work Experience"].get()
        hire_date = self.entries["Hire Date"].get()
        salary = self.entries["Salary"].get()
        shift_timings = self.entries["Shift Timings"].get()

        # Check if mandatory fields are filled
        if not staff_name or not designation or not phone:
            messagebox.showwarning("Input Error", "Please fill in all required fields (Name, Designation, Phone Number).")
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

            # Perform the update query
            update_query = """
                UPDATE staff 
                SET Staff_name = %s, Gender = %s, Staff_nationality = %s, Staff_Designation = %s, 
                    Staffphone_no = %s, Work_experience = %s, Hire_date = %s, Salary = %s, Shift_timings = %s
                WHERE Staff_id = %s
            """
            cursor.execute(update_query, (
                staff_name, gender, nationality, designation, phone, work_experience, hire_date, salary, shift_timings, staff_id
            ))
        
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Staff details updated successfully!")
        
            # Reset form and refresh the Treeview table
            self.reset_form()
            self.display_staff()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    def delete_staff(self):
        # Get selected item from Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a staff member to delete.")
            return

        staff_id = self.tree.item(selected_item)["values"][0]

        # Confirm before deleting
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this staff member?")
        if not confirm:
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

            # Delete the selected staff member from the database
            cursor.execute("DELETE FROM staff WHERE Staff_id = %s", (staff_id,))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Staff details deleted successfully!")
            self.display_staff()  # Refresh the table after deletion

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def reset_form(self):
        # Clear all input fields
        for entry in self.entries.values():
            if isinstance(entry, ctk.CTkOptionMenu):
                entry.set("Select")  # Reset dropdown menus
            else:
                entry.delete(0, 'end')  # Clear text fields


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: "light", "dark", "system"
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"
    
    root = ctk.CTk()
    app = StaffInfo(root)
    root.mainloop()