import customtkinter as ctk
import os
import sys
import re
import json
from tkinter import messagebox
from PIL import Image, ImageDraw

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
    window.geometry("1280x720")
    window.title("Study Planner - Dashboard")
    window.configure(fg_color="#D3D3D3")
    
    checkboxes = []

    def got_logout(event=None):
        window.destroy()
        from main import create_window
        main_window = create_window()
        main_window.mainloop()

    def validate_date():
        date = date_entry.get()
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date):
            messagebox.showerror("Error", "Please enter date in DD/MM/YYYY format")
            return False
        return True

    def save_new_subject(new_add):
        file_path = "task.json"
        data = load_json_file(file_path)
        data.append(new_add)
        
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except IOError as e:
            print(f"Error saving task: {e}")
            return False

    def addtask():
        tasksubject = entry_add.get()
        taskdescription = entry_disc.get("0.0", "end").strip()
        date = date_entry.get()
        
        if not all([tasksubject, taskdescription, date]):
            status_label.configure(text="Please fill all fields", text_color="red")
            frame.after(2000, lambda: status_label.configure(text=""))
            return
        
        if not validate_date():
            return
        
        subjectadd = {
            "subject": tasksubject,
            "Description": taskdescription,
            "Deadline": date
        }
        
        if save_new_subject(subjectadd):
            status_label.configure(text="Subject Add Successful!", text_color="green")
            display_tasks()  # Refresh the task list
        else:
            status_label.configure(text="Error saving task", text_color="red")
        frame.after(2000, lambda: status_label.configure(text=""))

    def display_tasks():
        nonlocal checkboxes
        checkboxes = []  # Reset checkboxes list
        file_path = "task.json"
        
        for widget in frame_view.winfo_children():
            widget.destroy()

        data = load_json_file(file_path)
        
        if isinstance(data, list):
            for idx, task in enumerate(data, start=1):
                subject = task.get("subject", "No Subject")
                description = task.get("Description", "No Description")
                deadline = task.get("Deadline", "No Deadline")

                task_text = f"{idx}. Subject: {subject}\n   Description: {description}\n   Deadline: {deadline}"

                task_frame = ctk.CTkFrame(frame_view,fg_color="lavender")
                task_frame.pack(fill="x", pady=5, padx=10)

                label = ctk.CTkLabel(task_frame, text=task_text, 
                                    font=("Segoe UI", 15, "bold"), anchor="w", justify="left")
                label.pack(anchor="w", padx=1, pady=10)
                
                check = ctk.CTkCheckBox(task_frame, text="", command=update_progress)
                check.pack(side="left", padx=5)
                checkboxes.append(check)
        else:
            ctk.CTkLabel(frame_view, text="No tasks found").pack()

    def update_progress():
        total = len(checkboxes)
        completed = sum(1 for cb in checkboxes if cb.get() == 1)
        
        if total > 0:
            percentage = int((completed / total) * 100)
            progress_bar.set(completed / total)
            progress_label.configure(text=f"Progress: {percentage}% ({completed}/{total})")

    def frame_open():
        frame.place(x=50, y=340) if not frame.winfo_ismapped() else frame.place_forget()

    def framev_open():
        frame_view.place(x=450, y=390) if not frame_view.winfo_ismapped() else frame_view.place_forget()
        display_tasks()  # Refresh tasks when opening

    def framep_open():
        frame_pro.place(x=860, y=340) if not frame_pro.winfo_ismapped() else frame_pro.place_forget()

    def frames_open(event=None):
        setting.place(x=10, y=70) if not setting.winfo_ismapped() else setting.place_forget()

    # Image handling with error fallback
    try:
        img_path = resource_path("assest/logo.png")
        size = (250, 250)
        image = Image.open(img_path).resize(size).convert("RGBA")
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        image.putalpha(mask)
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=size)
    except Exception as e:
        print(f"Error loading image: {e}")
        ctk_image = ctk.CTkImage(light_image=Image.new("RGBA", size, (0,0,0,0)), 
                           dark_image=Image.new("RGBA", size, (0,0,0,0)), 
                           size=size)

    label_image = ctk.CTkLabel(master=window, image=ctk_image, text="", corner_radius=10)
    label_image.place(x=470, y=10)

    title = ctk.CTkLabel(window, text="Welcome Back😊", font=("Segoe UI", 50, "bold"))
    title.place(x=430, y=260)

    # Add Task Section
    button_add = ctk.CTkButton(window, text="Add Task", width=250, height=50,
                              font=("Segoe UI", 20, "bold"), fg_color="#24a0ed", command=frame_open)
    button_add.place(x=90, y=280)

    frame = ctk.CTkScrollableFrame(window, width=330, height=300, fg_color="lavender")
    frame.place(x=50, y=340)

    add_task = ctk.CTkLabel(frame, text="Add subject:", font=("Segoe UI", 20, "bold"))
    add_task.pack(pady=10)

    subject = ctk.CTkLabel(frame, text="Enter Subject Name:", font=("Segoe UI", 15, "bold"))
    subject.pack(pady=2)
    entry_add = ctk.CTkEntry(frame, placeholder_text="Subject")
    entry_add.pack(pady=2)

    description = ctk.CTkLabel(frame, text="Enter Description (10-20 words):", font=("Segoe UI", 15, "bold"))
    description.pack(pady=2)
    entry_disc = ctk.CTkTextbox(frame, height=80)
    entry_disc.pack(pady=2)

    deadline = ctk.CTkLabel(frame, text="Enter Deadline:", font=("Segoe UI", 15, "bold"))
    deadline.pack(pady=2)
    date_entry = ctk.CTkEntry(frame, placeholder_text="DD/MM/YYYY")
    date_entry.pack(pady=2)

    submit = ctk.CTkButton(frame, width=40, height=20, text="Submit",
                          font=("Segoe UI", 15, "bold"), command=addtask)
    submit.pack(pady=15)

    status_label = ctk.CTkLabel(master=frame, text="", text_color="red", font=("Segoe UI", 15))
    status_label.pack(pady=10)

    # View Task Section
    button_view = ctk.CTkButton(window, text="View Task", width=250, height=50,
                               font=("Segoe UI", 20, "bold"), fg_color="#24a0ed", command=framev_open)
    button_view.place(x=500, y=330)

    frame_view = ctk.CTkScrollableFrame(window, width=330, height=300, fg_color="lavender")
    frame_view.place(x=450, y=390)
    display_tasks()  # Initial display

    # Progress Section
    button_pro = ctk.CTkButton(window, text="Show Progress", width=250, height=50,
                              font=("Segoe UI", 20, "bold"), fg_color="#24a0ed", command=framep_open)
    button_pro.place(x=890, y=280)

    frame_pro = ctk.CTkScrollableFrame(window, width=330, height=300, fg_color="lavender")
    frame_pro.place(x=860, y=340)

    progress_bar = ctk.CTkProgressBar(frame_pro, width=300)
    progress_bar.pack() 
    progress_bar.set(0)

    motivation_label = ctk.CTkLabel(frame_pro, text="Keep going, you're doing great! 💪", 
                                  font=("Segoe UI", 20, "italic"))
    motivation_label.pack(pady=5)

    progress_label = ctk.CTkLabel(frame_pro, text="Progress: 0%", font=("Segoe UI", 15, "bold"))
    progress_label.pack()  

    # Settings Section
    setting = ctk.CTkFrame(window, width=250, height=650, fg_color="lavender")
    
    ctk.CTkLabel(setting, text="                                ", font=("Segoe UI", 20, "bold")).place(x=1, y=1)
    ctk.CTkLabel(setting, text="HOME 🏠", font=("Segoe UI", 20, "bold")).place(x=1, y=10)
    ctk.CTkLabel(setting, text="ABOUT US ℹ️", font=("Segoe UI", 20, "bold")).place(x=1, y=50)
    ctk.CTkLabel(setting, text="FAQS/HELP ❓", font=("Segoe UI", 20, "bold")).place(x=1, y=100)
    
    logout = ctk.CTkLabel(setting, text="LOGOUT 🔒", font=("Segoe UI", 20, "bold"))
    logout.place(x=1, y=150)
    logout.bind("<Button-1>", got_logout)

    move = ctk.CTkLabel(window, text="⚙️", font=("Segoe UI", 30, "bold"), cursor="hand2")
    move.place(x=10, y=30)
    move.bind("<Button-1>", frames_open)

    def animate_image(x):
        if x > 800:
            x -= 10
            label_image.place(x=x, y=10)
            window.after(10, lambda: animate_image(x))
        else:
            label_image.place(x=470, y=10)

    window.after(100, lambda: animate_image(1300))
    
    return window

if __name__ == "__main__":
    window = create_window()
    window.mainloop()