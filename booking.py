import customtkinter as ctk
import mysql.connector
from tkinter import messagebox, ttk, Toplevel, Text, filedialog
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class BookingInfo:
    def __init__(self, root):
        self.root = root
        self.root.title("Booking Info")
        self.root.geometry("1540x840")

        # Frame setup
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Booking Form
        details_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        details_frame.grid(row=0, column=0, padx=20, pady=70, sticky="ne")
        ctk.CTkLabel(main_frame, text="Add a new booking", text_color="#1F538D", font=("Arial Black", 20)).place(x=170, y=25)

        # Labels and Entry Fields
        labels = ["Customer ID", "Customer Name", "Room Number", "Booking Date", "Check-in Date", "Check-out Date", "Number of Customers", "Room Charge", "Total Amount"]
        self.entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(details_frame, text=f"{label}:").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            if label in ["Booking Date", "Check-in Date", "Check-out Date"]:
                entry = DateEntry(details_frame, width=30, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            else:
                entry = ctk.CTkEntry(details_frame, width=300)

            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[label] = entry
            if label in ["Customer Name", "Room Charge", "Total Amount"]:
                entry.configure(state="disabled")

        # Buttons for operations
        self.save_button = ctk.CTkButton(details_frame, text="Save", command=self.save_booking)
        self.save_button.grid(row=10, column=0, padx=10, pady=10)

        self.update_button = ctk.CTkButton(details_frame, text="Update", command=self.update_booking)
        self.update_button.grid(row=10, column=1, padx=10, pady=10)

        self.delete_button = ctk.CTkButton(details_frame, text="Delete", command=self.delete_booking)
        self.delete_button.grid(row=11, column=0, padx=10, pady=10)

        self.reset_button = ctk.CTkButton(details_frame, text="Reset", command=self.reset_form)
        self.reset_button.grid(row=11, column=1, padx=10, pady=10)
        
        # Adding the Print Bill button
        self.print_bill_button = ctk.CTkButton(details_frame, text="Print Bill", command=self.print_bill)
        self.print_bill_button.grid(row=12, column=0, padx=10, pady=10)

        # Search bar setup at the top of the display area
        search_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        search_frame.grid(row=0, column=1, padx=20, pady=20, sticky="se")

        # Dropdown for selecting attribute and text box for input
        self.search_attr_var = ctk.StringVar(value="Select Attribute")
        attributes = ["Booking ID", "Customer ID", "Customer Name", "Room Number", "Booking Date", "Check-in Date", "Check-out Date", "Number of Customers", "Room Charge", "Total Amount"]
        self.attribute_menu = ctk.CTkOptionMenu(search_frame, variable=self.search_attr_var, values=attributes, width=150)
        self.attribute_menu.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(search_frame, width=150)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ctk.CTkButton(search_frame, text="Search", fg_color="green", width=100, command=self.search_booking)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.show_all_button = ctk.CTkButton(search_frame, text="Show All", fg_color="green", width=100, command=self.display_booking)
        self.show_all_button.grid(row=0, column=3, padx=10, pady=10)

        # Treeview Table for displaying booking records
        columns = ("Booking ID", "Customer ID", "Customer Name", "Room Number", "Booking Date", "Check-in Date", "Check-out Date", "Number of Customers", "Room Charge", "Total Amount")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        self.tree.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="ne")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Call method to display bookings
        self.display_booking()
        self.tree.bind("<ButtonRelease-1>", self.get_selected_row)

        self.print_bill_button = ctk.CTkButton(details_frame, text="Print Bill", command=self.print_bill)
        self.print_bill_button.grid(row=12, column=0, padx=10, pady=10)

    def save_booking(self):
        try:
            customer_id = self.entries["Customer ID"].get()
            room_no = self.entries["Room Number"].get()
            booking_date = self.entries["Booking Date"].get()
            check_in_date = self.entries["Check-in Date"].get()
            check_out_date = self.entries["Check-out Date"].get()
            num_of_customers = self.entries["Number of Customers"].get()

            connection = mysql.connector.connect(host="localhost", user="root", password="kbot", database="hotel_management")
            cursor = connection.cursor()

            cursor.execute("SELECT availability_status FROM room WHERE room_no = %s", (room_no,))
            room_status = cursor.fetchone()
            if not room_status:
                messagebox.showwarning("Not Found", "Room Number does not exist.")
                return
            elif room_status[0] == "Occupied":
                messagebox.showinfo("Room Occupied", "The selected room is currently occupied. Please choose an available room.")
                return

            cursor.execute("SELECT customer_name FROM customers WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()
            if customer:
                customer_name = customer[0]
                self.entries["Customer Name"].configure(state="normal")
                self.entries["Customer Name"].delete(0, 'end')
                self.entries["Customer Name"].insert(0, customer_name)
                self.entries["Customer Name"].configure(state="disabled")
            else:
                messagebox.showwarning("Not Found", "Customer ID does not exist.")
                return

            cursor.execute("SELECT room_type, view_type FROM room WHERE room_no = %s", (room_no,))
            room_data = cursor.fetchone()
            if room_data:
                room_type, view_type = room_data

                room_charge = 5000 if room_type == "Single" else 9000 if room_type == "Double" else 18000 if room_type == "Suite" else None
                if room_charge is None:
                    messagebox.showerror("Data Error", "Unknown room type.")
                    return

                room_charge += 4000 if view_type == "pool" else 2500 if view_type == "garden" else 0
                total_amount = room_charge * 1.18

                self.entries["Room Charge"].configure(state="normal")
                self.entries["Room Charge"].delete(0, 'end')
                self.entries["Room Charge"].insert(0, f"{room_charge:.2f}")
                self.entries["Room Charge"].configure(state="disabled")

                self.entries["Total Amount"].configure(state="normal")
                self.entries["Total Amount"].delete(0, 'end')
                self.entries["Total Amount"].insert(0, f"{total_amount:.2f}")
                self.entries["Total Amount"].configure(state="disabled")
            else:
                messagebox.showwarning("Not Found", "Room Number does not exist.")
                return

            cursor.execute(
                "INSERT INTO bookingw (customer_id, customer_name, room_no, booking_date, check_in_date, check_out_date, num_of_customers, room_charge) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (customer_id, customer_name, room_no, booking_date, check_in_date, check_out_date, num_of_customers, room_charge)
            )
            cursor.execute("UPDATE room SET availability_status = 'Occupied' WHERE room_no = %s", (room_no,))
            connection.commit()
            messagebox.showinfo("Success", "Booking saved successfully!")
            self.reset_form()
            self.display_booking()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if connection.is_connected():
                connection.close()

    def delete_booking(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a booking to delete.")
            return

        booking_id = self.tree.item(selected_item)["values"][0]
        room_no = self.tree.item(selected_item)["values"][1]  # Assuming the room_no is the second value in your tree

        try:
            # Connect to the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="kbot",
                database="hotel_management",
            )
            cursor = connection.cursor()

            # Perform delete query
            cursor.execute("DELETE FROM bookingw WHERE booking_id = %s", (booking_id,))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Booking deleted successfully!")

            # Call the function to change room availability status
            self.room_info.change_availability_status(room_no)  # Call the function with the room_no

            self.display_booking()  # Refresh the booking display

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    
    def update_booking(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a booking to update.")
            return

        booking_id = self.tree.item(selected_item)["values"][0]
        try:
            customer_id = self.entries["Customer ID"].get()
            room_no = self.entries["Room Number"].get()
            booking_date = self.entries["Booking Date"].get()
            check_in_date = self.entries["Check-in Date"].get()
            check_out_date = self.entries["Check-out Date"].get()
            num_of_customers = self.entries["Number of Customers"].get()

            connection = mysql.connector.connect(host="localhost", user="root", password="kbot", database="hotel_management")
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE bookingw 
                SET customer_id = %s, room_no = %s, booking_date = %s, check_in_date = %s, check_out_date = %s, num_of_customers = %s
                WHERE booking_id = %s
                """, (customer_id, room_no, booking_date, check_in_date, check_out_date, num_of_customers, booking_id)
            )
            connection.commit()
            messagebox.showinfo("Success", "Booking updated successfully!")
            self.reset_form()
            self.display_booking()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def display_booking(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="kbot", database="hotel_management")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bookingw")
            rows = cursor.fetchall()
            connection.close()

            for row in rows:
                self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def search_booking(self):
        attribute = self.search_attr_var.get()
        search_value = self.search_entry.get()

        if not attribute or not search_value:
            messagebox.showwarning("Input Error", "Please select an attribute and enter a value to search.")
            return

        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="kbot", database="hotel_management")
            cursor = connection.cursor()
            column_map = {
                "Booking ID": "booking_id",
                "Customer ID": "customer_id",
                "Customer Name": "customer_name",
                "Room Number": "room_no",
                "Booking Date": "booking_date",
                "Check-in Date": "check_in_date",
                "Check-out Date": "check_out_date",
                "Number of Customers": "num_of_customers",
                "Room Charge": "room_charge",
                "Total Amount": "total_amount"
            }

            query = f"SELECT * FROM bookingw WHERE {column_map[attribute]} LIKE %s"
            cursor.execute(query, (f"%{search_value}%",))
            rows = cursor.fetchall()
            connection.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in rows:
                self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def get_selected_row(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        row_values = self.tree.item(selected_item, "values")
        for i, label in enumerate(self.entries.keys()):
            self.entries[label].configure(state="normal")
            self.entries[label].delete(0, 'end')
            self.entries[label].insert(0, row_values[i+1])  
            if label in ["Customer Name", "Room Charge", "Total Amount"]:
                self.entries[label].configure(state="disabled")       

    def reset_form(self):
        for label, entry in self.entries.items():
            entry.configure(state="normal")
            entry.delete(0, 'end')
            if label in ["Customer Name", "Room Charge", "Total Amount"]:
                entry.configure(state="disabled")
    def print_bill(self):
        # Get selected booking from the tree
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a booking to print.")
            return

        # Retrieve booking details from selected row
        row_values = self.tree.item(selected_item, "values")

        # Prepare styled bill content for display
        bill_content = f"""KPC Hotels....\n\n
        Booking ID: {row_values[0]}\n
        Customer ID: {row_values[1]}\n
        Customer Name: {row_values[2]}\n
        Room Number: {row_values[3]}\n
        Booking Date: {row_values[4]}\n
        Check-in Date: {row_values[5]}\n
        Check-out Date: {row_values[6]}\n
        Number of Customers: {row_values[7]}\n
        Room Charge: {row_values[8]}\n
        Total Amount: {row_values[9]}\n
        \nThank you for choosing us!\n"""

        # Display styled bill content in a new window
        bill_window = Toplevel(self.root)
        bill_window.title("Bill")
        bill_window.geometry("400x500")

        bill_text = Text(bill_window, wrap="word", font=("Arial", 12), padx=20, pady=20, bg="#f0f0f0")
        bill_text.insert("1.0", bill_content)
        bill_text.config(state="disabled")
        bill_text.pack(expand=True, fill="both")

        # Generate PDF when clicking "Generate PDF" button
        def generate_pdf():
            pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not pdf_filename:
                return

            # Create the PDF
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            title_style = ParagraphStyle(
                "Title",
                parent=styles["Heading1"],
                fontSize=16,
                alignment=1,
                textColor=colors.darkblue
            )
            elements.append(Paragraph("KPC Hotels....", title_style))
            elements.append(Spacer(1, 12))

            # Format data as table for PDF
            data = [
                ["Booking ID", row_values[0]],
                ["Customer ID", row_values[1]],
                ["Customer Name", row_values[2]],
                ["Room Number", row_values[3]],
                ["Booking Date", row_values[4]],
                ["Check-in Date", row_values[5]],
                ["Check-out Date", row_values[6]],
                ["Number of Customers", row_values[7]],
                ["Room Charge", row_values[8]],
                ["Total Amount", row_values[9]],
            ]

            table = Table(data, colWidths=[150, 200])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("Thank you for choosing us!", styles["Normal"]))

            # Build PDF
            doc.build(elements)
            messagebox.showinfo("PDF Generated", f"PDF saved as {pdf_filename}")

        # Add "Generate PDF" button
        generate_pdf_button = ctk.CTkButton(bill_window, text="Generate PDF", command=generate_pdf)
        generate_pdf_button.pack(pady=10)

# Initialize and run the app
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = BookingInfo(root)
    root.mainloop()