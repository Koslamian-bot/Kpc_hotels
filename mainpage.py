import customtkinter as ctk
from PIL import Image, ImageDraw
import subprocess
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import numpy as np

def open_cus():
    subprocess.Popen(["python", "customer.py"])

def open_staff():
    subprocess.Popen(["python", "staff.py"])  

def open_rooms():
    subprocess.Popen(["python", "rooms.py"])  

def open_booking():
    subprocess.Popen(["python", "booking.py"])

def open_diary():
    subprocess.Popen(["python", "diary.py"])    

def exitapp():
    app.destroy()    

def fetch_room_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="kbot",
        database="hotel_management",
    )
    cursor = connection.cursor()
    
    # Query to count available and occupied rooms
    cursor.execute("SELECT availability_status, COUNT(*) FROM room GROUP BY availability_status")
    data = cursor.fetchall()
    connection.close()
    
    available_count = 0
    occupied_count = 0
    
    # Parse the data
    for status, count in data:
        if status == "Available":
            available_count = count
        elif status == "Occupied":
            occupied_count = count
    
    return available_count, occupied_count

# Function to display the pie chart
def display_pie_chart():
    available, occupied = fetch_room_data()
    
    # Pie chart data
    labels = ["Available", "Occupied"]
    sizes = [available, occupied]
    colors = ["#4CAF50", "#FF5733"]  # Green for available, red for occupied
    
    # Create a matplotlib figure for the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'color': "black"})
    ax.set_title("Room Availability", color="black")
    
    # Display the pie chart in the customtkinter frame
    canvas = FigureCanvasTkAgg(fig, master=bg_frame)  # Display on the main frame
    canvas.draw()
    canvas.get_tk_widget().place(x=1200, y=220)  # Position on the right side

# Function to crop image into a circle
def crop_circle(image_path, size):
    img = Image.open(image_path).resize(size, Image.LANCZOS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    result = Image.new('RGBA', size)
    result.paste(img, (0, 0), mask)
    return result

# Function to create and embed the 3D bar graph
def create_3d_bar_graph(frame):
    # Connect to MySQL Database
    connection = mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="kbot",  
        database="hotel_management"     
    )

    cursor = connection.cursor()

    # Query to fetch booking data (year, month, count)
    query = """
    SELECT YEAR(check_in_date) AS year, MONTH(check_in_date) AS month, COUNT(booking_id) AS booking_count
    FROM bookingw
    GROUP BY YEAR(check_in_date), MONTH(check_in_date)
    ORDER BY year, month;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()

    # Check if data is empty
    if not data:
        print("No data available to plot.")
        return  # Exit the function if no data

    # Prepare data for plotting
    years = np.unique([row[0] for row in data])  # Unique years
    months = np.array(range(1, 13))  # Months from 1 to 12
    booking_counts = np.zeros((len(years), len(months)))  # Initialize counts

    # Populate the booking_counts array
    for row in data:
        year_idx = np.where(years == row[0])[0][0]
        month_idx = row[1] - 1  # Months are 1-indexed
        booking_counts[year_idx, month_idx] = row[2]

    # Create the 3D bar graph
    fig = plt.figure(figsize=(8,9), facecolor='white')
    ax = fig.add_subplot(111, projection='3d', facecolor='white')
      # Transparent background

    x_data, y_data = np.meshgrid(years, months, indexing='ij')
    xpos = x_data.flatten()
    ypos = y_data.flatten()
    zpos = np.zeros_like(xpos)

    dx = np.ones_like(xpos) * 2 # Width of the bars
    dy = np.ones_like(ypos) * 2  # Depth of the bars
    dz = booking_counts.flatten()  # Height of the bars

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#23626b', alpha=0.7)

    # Set labels and ticks
    ax.set_xlabel('Year', color="black",fontsize=15)
    ax.set_zlabel('Booking Count', color="black",fontsize=15)
    ax.set_title('Monthly Booking Counts',fontsize=30)

    ax.set_xticks(years)
    ax.set_yticks(months)
    ax.set_xticklabels(years, color="black", fontsize=10) 
    ax.set_yticklabels(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'], 
        rotation=90, ha='center', fontsize=11,color="black"
    )


    # Create a canvas and embed the graph into the specified frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().configure(bg="white")
    canvas.get_tk_widget().pack()
  



# Initialize the main app window
app = ctk.CTk()
app.title("Main page")
app.geometry("1540x840")

# Set the dark theme for the app
ctk.set_appearance_mode("dark")

# Create the background using a CTkFrame with a dark color
bg_frame = ctk.CTkFrame(app, fg_color="white")
bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

# Sidebar creation (left column)
sidebar = ctk.CTkFrame(app, width=300, fg_color="#23626b")  # Set a dark grey sidebar
sidebar.place(x=0, y=0, relheight=1)

# Load and crop logo as a circle
circle_logo = crop_circle(r"C:\wtf\wtf images\WhatsApp Image 2024-10-13 at 19.52.58_7e41c5c6.jpg", (60, 60))

# Convert to CTkImage
logo_ctk_image = ctk.CTkImage(light_image=circle_logo, size=(60, 60))

# Add the logo to the sidebar using CTkImage and place it at the top-left corner
logo_label = ctk.CTkLabel(sidebar, image=logo_ctk_image, text="")
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")  # Top-left alignment using sticky="nw"

# Add a title above the buttons
title_label = ctk.CTkLabel(
    sidebar, 
    text="Menu", 
    text_color="white",  # Space grey text color
    font=("Arial Black", 20)  # Using Arial Black-like font
)
title_label.grid(row=1, column=0, padx=10, pady=(20, 10))  # Space between title and logo

# Add buttons to the sidebar with a curved radius of 32 and dark grey background
button_params = {
    "corner_radius": 32,
    "fg_color": "#23626b",
    "hover_color": "grey30",
    "text_color": "white",
    "anchor": "w",  # 'w' aligns content to the left (west)
    
}

btn1 = ctk.CTkButton(sidebar, text="Customer    ▸", font=("Arial", 16, "bold"), **button_params,command=open_cus)
btn1.grid(row=2, column=0, padx=20, pady=15)

btn2 = ctk.CTkButton(sidebar, text="Rooms        ▸", font=("Arial", 16, "bold"), **button_params,command=open_rooms)
btn2.grid(row=3, column=0, padx=20, pady=15)

btn3 = ctk.CTkButton(sidebar, text="Bookings    ▸", font=("Arial", 16, "bold"), **button_params,command=open_booking)
btn3.grid(row=4, column=0, padx=20, pady=15)

btn4 = ctk.CTkButton(sidebar, text="Staffs          ▸", font=("Arial", 16, "bold"), **button_params,command=open_staff)
btn4.grid(row=5, column=0, padx=20, pady=15)

btn5 = ctk.CTkButton(sidebar, text="Diary          ▸", font=("Arial", 16, "bold"), **button_params,command=open_diary)
btn5.grid(row=6, column=0, padx=20, pady=15)

btn6 = ctk.CTkButton(sidebar, text="Exit             ▸", font=("Arial", 16, "bold"), **button_params, command=exitapp)
btn6.grid(row=7, column=0, padx=20, pady=15)


# Box section
bw = 420  # Example width (adjust based on your requirement)
bh = 120  # Height of the box

# Box 1: Room Count
b1 = ctk.CTkFrame(bg_frame, width=bw, height=bh, fg_color="#23626b", corner_radius=15)  # Set corner_radius=0 for rectangular corners
b1.place(x=200, y=50)

bh1 = ctk.CTkLabel(b1, text="Room Count", text_color="white", font=("Arial Black", 24))
bh1.place(relx=0.5, rely=0.3, anchor="center")

bl1 = ctk.CTkLabel(b1, text="100", text_color="white", font=("Arial Black", 24))
bl1.place(relx=0.5, rely=0.7, anchor="center")

# Box 2: Staff Count
b2 = ctk.CTkFrame(bg_frame, width=bw, height=bh, fg_color="#23626b", corner_radius=15)
b2.place(x=640, y=50)

bh2 = ctk.CTkLabel(b2, text="Staff Count", text_color="white", font=("Arial Black", 24))
bh2.place(relx=0.5, rely=0.3, anchor="center")

bl2 = ctk.CTkLabel(b2, text="150", text_color="white", font=("Arial Black", 24))
bl2.place(relx=0.5, rely=0.7, anchor="center")

# Box 3: Ratings
b3 = ctk.CTkFrame(bg_frame, width=bw, height=bh, fg_color="#23626b", corner_radius=15)
b3.place(x=1080, y=50)

bh3 = ctk.CTkLabel(b3, text="Ratings", text_color="white", font=("Arial Black", 24))
bh3.place(relx=0.5, rely=0.3, anchor="center")

bl3 = ctk.CTkLabel(b3, text="4.7", text_color="white", font=("Arial Black", 24))
bl3.place(relx=0.5, rely=0.7, anchor="center")

# Graph Section
graph_frame = ctk.CTkFrame(bg_frame, fg_color="white", width=1, height=5, corner_radius=15)
graph_frame.place(x=180, y=180)

# Display 3D Bar Graph
create_3d_bar_graph(graph_frame)

#sponsors page
sp = ctk.CTkFrame(bg_frame, width=650, height=250, fg_color="white", corner_radius=15)
sp.place(x=870, y=550)

spon = ctk.CTkImage(light_image=Image.open(r"C:\wtf\wtf images\all.jpg"), size=(450,280))
spon = ctk.CTkLabel(sp, image=spon, text="") 
spon.place(x=100, y=-20)  

display_pie_chart()

app.mainloop()