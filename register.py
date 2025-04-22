from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # pip install pillow
import sqlite3
import os

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # ====== Background Image ======
        self.bg = ImageTk.PhotoImage(file="images/b2.jpg")
        bg = Label(self.root, image=self.bg).place(x=250, y=0, relwidth=1, relheight=1)

        # ====== Side Image ======
        self.left = ImageTk.PhotoImage(file="images/side.png")
        left = Label(self.root, image=self.left).place(x=80, y=100, width=400, height=500)

        # ====== Registration Frame ======
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=100, width=700, height=500)

        title = Label(frame1, text="REGISTER HERE", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=50, y=30)

        # ======================= Row 1 =======================
        f_name = Label(frame1, text="First Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        l_name = Label(frame1, text="Last Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=100)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)

        # ======================= Row 2 =======================
        contact = Label(frame1, text="Contact No.", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=170)
        self.txt_contact = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=200, width=250)

        email = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=160)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=190, width=250)

        # ======================= Row 3 =======================
        question = Label(frame1, text="Security Question", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=240)
        self.cmb_question = ttk.Combobox(frame1, font=("times new roman", 13), state='readonly', justify=CENTER)
        self.cmb_question['values'] = ("Select", "Your First pet Name", "Your Birth Place", "Your Best Friend Name")
        self.cmb_question.place(x=50, y=270, width=250)
        self.cmb_question.current(0)

        answer = Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=240)
        self.txt_answer = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=370, y=270, width=250)

        password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=310)
        self.txt_password = Entry(frame1, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_password.place(x=50, y=340, width=250)

        cpassword = Label(frame1, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=310)
        self.txt_cpassword = Entry(frame1, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_cpassword.place(x=370, y=340, width=250)

        # ================ Terms & Conditions ================
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="I Agree The Terms & Conditions", variable=self.var_chk, onvalue=1, offvalue=0,
                          bg="white", font=("times new roman", 12)).place(x=50, y=380)

        self.btn_img = ImageTk.PhotoImage(file="images/register.png")
        btn_register = Button(frame1, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data).place(x=50, y=420)

        btn = Button(frame1, text="Sign In", command=self.login_window, font=("times new roman", 12), bg="lightpink", bd=0, cursor="hand2")
        btn.place(x=250, y=460, width=180)

        # Ensure table exists
        self.create_user_table()

    def login_window(self):
        self.root.destroy()
        os.system("python login.py")

    def clear(self):
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmb_question.current(0)

    def create_user_table(self):
        # Create table if not exists
        conn = sqlite3.connect(database="rms.db")
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            F_NAME TEXT,
            L_NAME TEXT,
            CONTACT TEXT,
            EMAIL TEXT UNIQUE,
            QUESTION TEXT,
            ANSWER TEXT,
            PASSWORD TEXT
        )
        """)
        conn.commit()
        conn.close()

    def register_data(self):
        if self.txt_fname.get() == "" or self.txt_contact.get() == "" or self.txt_email.get() == "" \
                or self.cmb_question.get() == "Select" or self.txt_password.get() == "" or self.txt_cpassword.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror("Error", "Password and Confirm Password should be same", parent=self.root)
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please agree to our Terms & Conditions", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database="rms.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM data WHERE email=?", (self.txt_email.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "User already exists, please try with another email", parent=self.root)
                else:
                    cur.execute("INSERT INTO data(F_NAME, L_NAME, CONTACT, EMAIL, QUESTION, ANSWER, PASSWORD) VALUES(?,?,?,?,?,?,?)",
                                (
                                    self.txt_fname.get(),
                                    self.txt_lname.get(),
                                    self.txt_contact.get(),
                                    self.txt_email.get(),
                                    self.cmb_question.get(),
                                    self.txt_answer.get(),
                                    self.txt_password.get()
                                ))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Registration Successful", parent=self.root)
                    self.clear()
                    self.login_window()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

# Launch the window
root = Tk()
obj = Register(root)
root.mainloop()
