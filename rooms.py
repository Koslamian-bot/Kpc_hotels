import customtkinter as ctk
import mysql.connector
from PIL import Image, ImageDraw
from tkinter import messagebox
from tkinter import ttk

class RoomInfo:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Info")
        self.root.geometry("1540x840")

        # Create a main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Right frame for search and options buttons (now at the top of the display area)
        button_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        button_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Dropdown for selecting attribute and text box for input
        self.search_attr_var = ctk.StringVar(value="Select Attribute")
        attributes = ["room_no", "room_type", "availability_status", "priceOfTheRoom", "has_ac", "view_type"]
        self.attribute_menu = ctk.CTkOptionMenu(button_frame, variable=self.search_attr_var, values=attributes, width=150)
        self.attribute_menu.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(button_frame, width=150)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ctk.CTkButton(button_frame, text="Search", fg_color="green", width=100, command=self.search_room)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.show_all_button = ctk.CTkButton(button_frame, text="Show All", fg_color="green", width=100, command=self.display_rooms)
        self.show_all_button.grid(row=0, column=3, padx=10, pady=10)

        # Button to change availability status
        self.change_status_button = ctk.CTkButton(button_frame, text="Change Status", fg_color="orange", width=100, command=self.change_availability_status)
        self.change_status_button.grid(row=0, column=4, padx=10, pady=10)

        # Treeview table for displaying rooms (moved to the left)
        columns = ("room_no", "room_type", "availability_status", "priceOfTheRoom", "has_ac", "Private_accomodation")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=40)
        self.tree.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Call method to display rooms
        self.display_rooms()
   

        spon = ctk.CTkImage(light_image=Image.open(r"C:\wtf\wtf images\rooms.png"), size=(700,670))
        spon = ctk.CTkLabel(main_frame, image=spon, text="") 
        spon.place(x=800, y=80)

    def display_rooms(self):
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
        cursor.execute("SELECT * FROM room;")  # Query the rooms table

        # Fetch all rows from the database
        rows = cursor.fetchall()
        connection.close()

        # Insert data into the Treeview widget
        for row in rows:
            self.tree.insert("", "end", values=row)

    def search_room(self):
        # Get the selected attribute and input value
        attribute = self.search_attr_var.get()
        search_value = self.search_entry.get()

        if not attribute or not search_value:
            messagebox.showwarning("Input Error", "Please select an attribute and enter a value to search.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()

            query = f"SELECT * FROM room WHERE {attribute} = %s"
            cursor.execute(query, (search_value,))
            rows = cursor.fetchall()
            connection.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in rows:
                self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def change_availability_status(self):
        # Get the selected room number
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a room from the list.")
            return
        
        room_no = self.tree.item(selected_item, "values")[0]  # Get the room_no from the selected row
        current_status = self.tree.item(selected_item, "values")[2]  # Get the current availability status
        
        # Toggle the availability status
        new_status = "Occupied" if current_status == "Available" else "Available"

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()

            query = "UPDATE room SET availability_status = %s WHERE room_no = %s"
            cursor.execute(query, (new_status, room_no))
            connection.commit()
            connection.close()

            # Update the Treeview
            self.tree.item(selected_item, values=(room_no, self.tree.item(selected_item, "values")[1], new_status, self.tree.item(selected_item, "values")[3], self.tree.item(selected_item, "values")[4], self.tree.item(selected_item, "values")[5]))

            messagebox.showinfo("Success", f"Room {room_no} availability changed to {new_status}.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    app = RoomInfo(root)
    root.mainloop()
