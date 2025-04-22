from tkinter import *
from PIL import Image, ImageTk, ImageDraw  # pip install pillow
from course import CourseClass
from student import StudentClass
from result import resultClass
from report import reportClass
from tkinter import messagebox
import os
from datetime import datetime
from math import sin, cos, radians
import sqlite3

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="WHITE")

        # === Icons ===
        try:
            self.logo_dash = ImageTk.PhotoImage(file="images/logo_p.png")
        except Exception:
            messagebox.showerror("Error", "Logo image not found!")
            self.logo_dash = None

        # === Title ===
        title = Label(
            self.root,
            text="Student Result Management System",
            padx=10,
            compound="left",
            image=self.logo_dash,
            font=("goudy old style", 20, "bold"),
            bg="#033054",
            fg="YELLOW"
        )
        title.place(x=0, y=0, relwidth=1, height=50)

        # === Menu ===
        M_FRAME = LabelFrame(self.root, text="Menus", font=("times new roman", 15), bg="WHITE")
        M_FRAME.place(x=10, y=70, width=1340, height=80)

        # === Buttons ===
        Button(M_FRAME, text="Courses", font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2", command=self.add_course).place(x=20, y=5, width=200, height=40)

        Button(M_FRAME, text="Students", font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2", command=self.add_student).place(x=240, y=5, width=200, height=40)

        Button(M_FRAME, text="Result", font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2", command=self.add_result).place(x=460, y=5, width=200, height=40)

        Button(M_FRAME, text="View", font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2", command=self.add_report).place(x=680, y=5, width=200, height=40)

        Button(M_FRAME, text="Logout", font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2", command=self.logout).place(x=900, y=5, width=200, height=40)

        Button(M_FRAME, text="Exit", font=("goudy old style", 15, "bold"),
               bg="#0b5377", fg="white", cursor="hand2", command=self.exit_).place(x=1120, y=5, width=200, height=40)

        # === Background Image ===
        try:
            self.bg_img = Image.open("images/bg.png").resize((920, 350), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            Label(self.root, image=self.bg_img).place(x=400, y=180, width=920, height=350)
        except Exception:
            messagebox.showerror("Error", "Background image not found!")

        # === Info Panels ===
        self.lbl_course = Label(self.root, text="Total Courses\n[ 0 ]", font=("goudy old style", 20),
                                bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_course.place(x=400, y=530, width=300, height=100)

        self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]", font=("goudy old style", 20),
                                 bd=10, relief=RIDGE, bg="#0676ad", fg="white")
        self.lbl_student.place(x=710, y=530, width=300, height=100)

        self.lbl_result = Label(self.root, text="Total Results\n[ 0 ]", font=("goudy old style", 20),
                                bd=10, relief=RIDGE, bg="#038074", fg="white")
        self.lbl_result.place(x=1020, y=530, width=300, height=100)

        # === Clock Widget ===
        self.lbl = Label(self.root, text="\nCLOCK", font=("Book Antiqua", 25, "bold"),
                         fg="white", compound="bottom", bg="black", bd=0)
        self.lbl.place(x=10, y=180, height=450, width=350)
        self.working()

        # === Footer ===
        Label(self.root, text="SRMS - Student Result Management System\nContact us for any technical issue: 987xxxx01",
              font=("goudy old style", 12), bg="#262626", fg="white").pack(side=BOTTOM, fill=X)

        self.update_details()

    # === Update Dashboard Info ===
    def update_details(self):
        try:
            with sqlite3.connect(database="rms.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM course")
                self.lbl_course.config(text=f"Total Courses\n[{len(cur.fetchall())}]")

                cur.execute("SELECT * FROM student")
                self.lbl_student.config(text=f"Total Students\n[{len(cur.fetchall())}]")

                cur.execute("SELECT * FROM result")
                self.lbl_result.config(text=f"Total Results\n[{len(cur.fetchall())}]")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        self.lbl_course.after(2000, self.update_details)

    # === Clock Working ===
    def working(self):
        now = datetime.now()
        hr = (now.hour / 12) * 360
        min_ = (now.minute / 60) * 360
        sec_ = (now.second / 60) * 360

        clock_image = self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(clock_image)
        self.lbl.config(image=self.img)
        self.lbl.after(1000, self.working)

    def clock_image(self, hr, min_, sec_):
        clock_image = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock_image)

        try:
            bg = Image.open("images/c.png").resize((300, 300), Image.LANCZOS)
            clock_image.paste(bg, (50, 50))
        except Exception:
            pass

        origin = 200
        draw.line((origin, origin,
                   origin + 50 * sin(radians(hr)),
                   origin - 50 * cos(radians(hr))), fill="#df005e", width=4)
        draw.line((origin, origin,
                   origin + 80 * sin(radians(min_)),
                   origin - 80 * cos(radians(min_))), fill="white", width=3)
        draw.line((origin, origin,
                   origin + 100 * sin(radians(sec_)),
                   origin - 100 * cos(radians(sec_))), fill="yellow", width=2)

        draw.ellipse((195, 195, 210, 210), fill="blue")
        return clock_image

    # === Navigation Commands ===
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentClass(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)

    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)

    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op:
            self.root.destroy()
            os.system("python login.py")

    def exit_(self):
        op = messagebox.askyesno("Confirm", "Do you really want to Exit?", parent=self.root)
        if op:
            self.root.destroy()


# === Run App ===
if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()
