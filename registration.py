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
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.geometry("1280x720")
    window.title("Study Planner - Registration")

    def check_login():
        window.destroy()
        from login import create_window
        login_window = create_window()
        login_window.mainloop()

    def save_new_user(new_user):
        file_path = "ufile.json"
        data = load_json_file(file_path)
        data.append(new_user)
        
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except IOError as e:
            print(f"Error saving user: {e}")
            return False

    def saved_jsonfile():
        firstname = entry_n1.get()
        lastname = entry_n2.get()
        email_user = entry_user.get()
        passwordu = entry_pass.get()
        repassword = entry_email.get()

        if not all([firstname, lastname, email_user, passwordu, repassword]):
            status_label.configure(text="Please fill all fields", text_color="red")
            window.after(2000, lambda: status_label.configure(text=""))
            return

        if "@" not in email_user or "." not in email_user:
            status_label.configure(text="Invalid email format", text_color="red")
            window.after(2000, lambda: status_label.configure(text=""))
            return
        
        if passwordu != repassword:
            status_label.configure(text="Passwords do not match", text_color="red")
            window.after(2000, lambda: status_label.configure(text=""))
            return
        
        user_signin = {
            "name": f"{firstname} {lastname}",
            "Email": email_user,
            "password": passwordu
        }

        if save_new_user(user_signin):
            status_label.configure(text="SignIn Successful!", text_color="green")
            window.after(2000, check_login)
        else:
            status_label.configure(text="Error saving data", text_color="red")

    # Background image with error handling
    try:
        img_id = resource_path("assest/img.png")
        bg_pil_image = Image.open(img_id)
        bg_ctk_image = ctk.CTkImage(light_image=bg_pil_image, dark_image=bg_pil_image, size=(1280, 1280))
        bg_label = ctk.CTkLabel(window, image=bg_ctk_image, text="") 
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading background image: {e}")
        window.configure(fg_color="#B6CBD8")

    frame = ctk.CTkFrame(master=window, width=450, height=550, fg_color="transparent")
    frame.pack(expand=True)
    frame.pack_propagate(False)
    frame.place(x=1300, y=150)

    label_head = ctk.CTkLabel(window, text="📖Study Planner", font=("Segoe UI", 50, "bold"), corner_radius=20)
    label_head.pack(pady=2)
    label_head.place(x=610, y=40)

    label_title = ctk.CTkLabel(master=frame, text="Sign In Form", font=("Segoe UI", 30, "bold"))
    label_title.pack(pady=20)

    label_n1 = ctk.CTkLabel(master=frame, text="Enter your first name:", font=("Segoe UI", 15, "bold"))
    label_n1.pack(pady=2)

    entry_n1 = ctk.CTkEntry(master=frame, width=250, corner_radius=10, placeholder_text="First Name")
    entry_n1.pack(pady=2)

    label_n2 = ctk.CTkLabel(master=frame, text="Enter your last name:", font=("Segoe UI", 15, "bold"))
    label_n2.pack(pady=2)

    entry_n2 = ctk.CTkEntry(master=frame, width=250, corner_radius=10, placeholder_text="Last Name")
    entry_n2.pack(pady=2)

    label_user = ctk.CTkLabel(master=frame, text="Enter your email:", font=("Segoe UI", 15, "bold"))
    label_user.pack(pady=2)

    entry_user = ctk.CTkEntry(master=frame, width=250, corner_radius=10, placeholder_text="Email")
    entry_user.pack(pady=2)

    label_pass = ctk.CTkLabel(master=frame, text="Enter your password:", font=("Segoe UI", 15, "bold"))
    label_pass.pack(pady=2)

    entry_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", width=250, corner_radius=10)
    entry_pass.pack(pady=4)

    label_email = ctk.CTkLabel(master=frame, text="Verify Password:", font=("Segoe UI", 15, "bold"))
    label_email.pack(pady=2)

    entry_email = ctk.CTkEntry(master=frame, width=250, corner_radius=10, 
                              placeholder_text="Verify Password", show="*")
    entry_email.pack(pady=1)

    button = ctk.CTkButton(master=frame, text="Submit", width=150, fg_color="#007acc", 
                          hover_color="#005f99", font=("Segoe UI", 15, "bold"), command=saved_jsonfile)
    button.pack(pady=20)

    status_label = ctk.CTkLabel(master=frame, text="", text_color="red", font=("Segoe UI", 15))
    status_label.pack(pady=10)

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