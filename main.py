import customtkinter as ctk
import os
import sys
from PIL import Image, ImageDraw

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    path = os.path.join(base_path, relative_path)
    
    if not os.path.exists(path):
        # Try without 'assest' folder if path contains it
        if "assest" in relative_path:
            alt_path = os.path.join(base_path, os.path.basename(relative_path))
            if os.path.exists(alt_path):
                return alt_path
        # Try different capitalization
        alt_path = os.path.join(base_path, relative_path.lower())
        if os.path.exists(alt_path):
            return alt_path
            
    return path

def open_login():
    window.destroy()
    from login import create_window
    login_window = create_window()
    login_window.mainloop()

def open_signin():
    window.destroy()
    from registration import create_window
    signin_window = create_window()
    signin_window.mainloop()

window = ctk.CTk()
window.title("Study Planner - Main")
window.geometry("1280x720")
window.configure(fg_color="black")

# Image handling with error fallback
try:
    img_path = resource_path("assest/logo.png")
    size = (300, 300)
    image = Image.open(img_path).resize(size).convert("RGBA")
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    image.putalpha(mask)
    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=size)
except Exception as e:
    print(f"Error loading image: {e}")
    # Create a blank image as fallback
    ctk_image = ctk.CTkImage(light_image=Image.new("RGBA", size, (0,0,0,0)), 
                           dark_image=Image.new("RGBA", size, (0,0,0,0)), 
                           size=size)

label_image = ctk.CTkLabel(master=window, image=ctk_image, text="", corner_radius=10)
label_image.place(x=1300, y=150)

label_heading = ctk.CTkLabel(window, text="Welcome To Study Planner😊", 
                            font=("Comic Sans MS", 50, "bold"), text_color="white")
label_heading.place(x=350, y=380)

button = ctk.CTkButton(window, text="Login", font=("Comic Sans MS", 20, "bold"),
                      hover_color="#005f99", width=200, height=40, command=open_login)
button.place(x=400, y=500)

button_sign = ctk.CTkButton(window, text="Sign In", font=("Comic Sans MS", 20, "bold"),
                           hover_color="#005f99", width=200, height=40, command=open_signin)
button_sign.place(x=700, y=500)

disc_label = ctk.CTkLabel(window, 
                         text="📘About App:\n📋This app helps you manage tasks\n📋Stay organized\n📋And boost your study habits.",
                         font=("Comic Sans MS", 15, "bold"), text_color="white")
disc_label.place(x=535, y=580)

def animate_image(x):
    if x > 800:
        x -= 10
        label_image.place(x=x, y=50)
        window.after(10, lambda: animate_image(x))
    else:
        label_image.place(x=470, y=50)

window.after(100, lambda: animate_image(1300))
window.mainloop()