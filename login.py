from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
from math import sin, cos, radians
import sqlite3
import os


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("LOGIN")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#022e2f")

        # === Background sections ===
        Label(self.root, bg="green", bd=0).place(x=0, y=0, relheight=1, width=600)
        Label(self.root, bg="purple", bd=0).place(x=600, y=0, relheight=1, relwidth=1)

        # === Login Frame ===
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=250, y=100, width=800, height=500)

        Label(login_frame, text="LOGIN HERE", font=("times new roman", 30, "bold"), bg="white", fg="#08a3d2").place(x=250, y=50)

        Label(login_frame, text="Email Address", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=150)
        self.txt_email = Entry(login_frame, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=250, y=180, width=350, height=35)

        Label(login_frame, text="Password", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=250)
        self.txt_pass = Entry(login_frame, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_pass.place(x=250, y=280, width=350, height=35)

        # === Buttons ===
        Button(login_frame, text="Register New Account", command=self.register_window,
               font=("times new roman", 14), bg="white", bd=0, fg="red", cursor="hand2").place(x=250, y=350)

        Button(login_frame, text="Forget Password", command=self.forgot_password_window,
               font=("times new roman", 14), bg="white", bd=0, fg="red", cursor="hand2").place(x=500, y=420)

        Button(login_frame, text="LOGIN", command=self.login,
               font=("times new roman", 20, "bold"), fg="white", bg="red", cursor="hand2").place(x=250, y=400, width=180, height=40)

        # === Clock ===
        self.lbl = Label(self.root, text="\nCLOCK", font=("Book Antiqua", 25, "bold"),
                         fg="white", compound="bottom", bg="black", bd=0)
        self.lbl.place(x=90, y=120, height=450, width=350)
        self.update_clock()

    # === Open Registration Window ===
    def register_window(self):
        self.root.destroy()
        import register  # Assumes register.py exists

    # === Handle Login ===
    def login(self):
        if self.txt_email.get() == "" or self.txt_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database="rms.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM data WHERE email=? AND password=?", 
                            (self.txt_email.get().strip(), self.txt_pass.get().strip()))
                row = cur.fetchone()
                conn.close()
                if row is None:
                    messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome: {self.txt_email.get()}", parent=self.root)
                    self.root.destroy()
                    os.system("python dashboard.py")  # Launch dashboard
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    # === Forgot Password Window ===
    def forgot_password_window(self):
        if self.txt_email.get() == "":
            messagebox.showerror("Error", "Please enter your email to reset password", parent=self.root)
            return

        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM data WHERE email=?", (self.txt_email.get(),))
            row = cur.fetchone()
            con.close()
            if row is None:
                messagebox.showerror("Error", "Email not found", parent=self.root)
            else:
                self.root2 = Toplevel()
                self.root2.title("Reset Password")
                self.root2.geometry("400x400+480+150")
                self.root2.config(bg="lightgray")
                self.root2.focus_force()
                self.root2.grab_set()

                Label(self.root2, text="Reset Password", font=("times new roman", 20, "bold"),
                      bg="white", fg="red").pack(fill=X)

                Label(self.root2, text="Security Question", font=("times new roman", 15, "bold"),
                      bg="lightgray", fg="black").place(x=50, y=60)
                self.cmb_question = ttk.Combobox(self.root2, font=("times new roman", 13), state='readonly')
                self.cmb_question['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
                self.cmb_question.place(x=50, y=90, width=300)
                self.cmb_question.current(0)

                Label(self.root2, text="Answer", font=("times new roman", 15, "bold"),
                      bg="lightgray").place(x=50, y=140)
                self.txt_answer = Entry(self.root2, font=("times new roman", 15), bg="white")
                self.txt_answer.place(x=50, y=170, width=300)

                Label(self.root2, text="New Password", font=("times new roman", 15, "bold"),
                      bg="lightgray").place(x=50, y=220)
                self.txt_new_pass = Entry(self.root2, font=("times new roman", 15), bg="white")
                self.txt_new_pass.place(x=50, y=250, width=300)

                Button(self.root2, text="Reset Password", command=self.reset_password,
                       bg="green", fg="white", font=("times new roman", 15, "bold")).place(x=120, y=300, width=160)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    # === Reset Password in DB ===
    def reset_password(self):
        if self.cmb_question.get() == "Select" or self.txt_answer.get() == "" or self.txt_new_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root2)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM data WHERE email=? AND question=? AND answer=?",
                            (self.txt_email.get(), self.cmb_question.get(), self.txt_answer.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Incorrect security details", parent=self.root2)
                else:
                    cur.execute("UPDATE data SET password=? WHERE email=?", 
                                (self.txt_new_pass.get(), self.txt_email.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Password updated successfully", parent=self.root2)
                    self.root2.destroy()
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root2)

    # === Create Clock Image ===
    def draw_clock(self, hr, min_, sec_):
        clock_image = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock_image)

        # Load background image
        bg = Image.open("images/c.png")
        bg = bg.resize((300, 300), Image.LANCZOS)
        clock_image.paste(bg, (50, 50))

        # Clock origin
        origin = 200, 200

        # Hour hand
        draw.line((origin, 200 + 50 * sin(radians(hr)), 200 - 50 * cos(radians(hr))),
                  fill="#df005e", width=4)

        # Minute hand
        draw.line((origin, 200 + 80 * sin(radians(min_)), 200 - 80 * cos(radians(min_))),
                  fill="white", width=3)

        # Second hand
        draw.line((origin, 200 + 100 * sin(radians(sec_)), 200 - 100 * cos(radians(sec_))),
                  fill="yellow", width=2)

        # Center point
        draw.ellipse((195, 195, 210, 210), fill="blue")

        clock_image.save("clock_new.png")

    # === Clock Working ===
    def update_clock(self):
        h = datetime.now().hour
        m = datetime.now().minute
        s = datetime.now().second

        hr = (h % 12) * 30  # 360/12
        min_ = m * 6        # 360/60
        sec_ = s * 6

        self.draw_clock(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(1000, self.update_clock)  # Update every second


# === Run Application ===
if __name__ == "__main__":
    root = Tk()
    obj = LoginWindow(root)
    root.mainloop()
