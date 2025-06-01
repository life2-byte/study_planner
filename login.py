import customtkinter as ctk
import os
import sys
import json
from PIL import Image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_json_file(filename):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {filename}: {e}")
        return []

def create_window():
    window = ctk.CTk()
    window.title("Study Planner - Login")
    window.geometry("1280x720")
    
    def check_signin(event=None):
        window.destroy()
        from registration import create_window
        signin_window = create_window()
        signin_window.mainloop()

    def open_main():
        window.destroy()
        from dashboard import create_window
        dashboard_window = create_window()
        dashboard_window.mainloop()

    def on_click(event):
        popup = ctk.CTkToplevel(window)
        popup.title("Password Reset")
        popup.geometry("400x300")
        
        show = ctk.CTkLabel(popup, text="Create New Password:", font=("Segoe UI", 10, "bold"))
        show.pack(pady=2)
        show_entry = ctk.CTkEntry(popup)
        show_entry.pack(pady=2)
        
        show = ctk.CTkLabel(popup, text="Verify Password:", font=("Segoe UI", 10, "bold"))
        show.pack(pady=2)
        show_entry1 = ctk.CTkEntry(popup)
        show_entry1.pack(pady=2)
        
        button_show = ctk.CTkButton(popup, width=100, text="Submit", command=popup.destroy)
        button_show.pack(pady=2)

    def check_user_credentials():
        email_entered = email_entry.get()
        password_entered = password_entry.get()

        users = load_json_file("ufile.json")
        
        for user in users:
            if user.get("Email") == email_entered and user.get("password") == password_entered:
                status_label.configure(text="Login Successful!", text_color="green")
                window.after(2000, open_main)
                return
            else:
                status_label.configure(text="Invalid Email Or Password", text_color="red")
                frame.after(2000, lambda: status_label.configure(text=""))

    # Background image with error handling
    try:
        img_id = resource_path("assest/image.png")
        bg_pil_image = Image.open(img_id)
        bg_ctk_image = ctk.CTkImage(light_image=bg_pil_image, dark_image=bg_pil_image, size=(1280, 720))
        bg_label = ctk.CTkLabel(window, image=bg_ctk_image, text="") 
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading background image: {e}")
        window.configure(fg_color="#B6CBD8")

    frame = ctk.CTkFrame(window, width=500, height=450, fg_color="#B6CBD8", bg_color="#B6CBD8")
    frame.pack(expand=True)
    frame.propagate(False)

    head = ctk.CTkLabel(window, text="📖Study Planner", font=("Segoe UI", 50, "bold"), corner_radius=20, bg_color="#88A9BB")
    head.pack(pady=2)
    head.place(x=640, y=50)

    title = ctk.CTkLabel(master=frame, text="Login Form", font=("Segoe UI", 30, "bold"))
    title.pack(pady=50)

    email = ctk.CTkLabel(master=frame, text="Enter Your Email:", font=("Segoe UI", 20, "bold"))
    email.pack()
    email.place(x=130, y=140)

    email_entry = ctk.CTkEntry(master=frame, corner_radius=10, width=250, fg_color="#DCE6EB", placeholder_text="Email")
    email_entry.pack()
    email_entry.place(x=125, y=170)

    password = ctk.CTkLabel(master=frame, text="Enter Your Password:", font=("Segoe UI", 20, "bold"))
    password.pack()
    password.place(x=130, y=220)

    password_entry = ctk.CTkEntry(master=frame, show="*", corner_radius=10, width=250, fg_color="#DCE6EB", placeholder_text="Password")
    password_entry.pack()
    password_entry.place(x=125, y=250)

    button = ctk.CTkButton(master=frame, text="Submit", width=150, fg_color="#007acc", 
                          hover_color="#005f99", font=("Segoe UI", 15, "bold"), command=check_user_credentials)
    button.pack()
    button.place(x=180, y=300)

    forget = ctk.CTkLabel(master=frame, text="Forget Password!", font=("Segoe UI", 16, "bold"), cursor="hand2")
    forget.place(x=190, y=340)
    forget.bind("<Button-1>", on_click)

    move = ctk.CTkLabel(master=frame, text="Don't Have a Account__SignIn", 
                       font=("Segoe UI", 16, "bold"), cursor="hand2")
    move.place(x=140, y=370)
    move.bind("<Button-1>", check_signin)

    status_label = ctk.CTkLabel(master=frame, text="", text_color="red", font=("Segoe UI", 15))
    status_label.place(x=180, y=400)

    def animate_frame(x):
        if x > 800:
            x -= 10
            frame.place(x=x, y=150)
            window.after(10, lambda: animate_frame(x))
        else:
            frame.place(x=600, y=150)

    window.after(100, lambda: animate_frame(1300))
    
    return window

if __name__ == "__main__":
    window = create_window()
    window.mainloop()