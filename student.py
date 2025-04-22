from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="WHITE")
        self.root.focus_force()

        # ====title====
        title = Label(self.root, text="Manage Student Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # =====variables=====
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_a_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()

        # =====widgets=======
        # ====col1=====
        Label(self.root, text="Roll No", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=60)
        Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=100)
        Label(self.root, text="Email", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=140)
        Label(self.root, text="Gender", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=180)
        Label(self.root, text="State", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=220)

        Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=150, y=220, width=150)
        Label(self.root, text="City", font=("goudy old style", 15, "bold"), bg='white').place(x=310, y=220)
        Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=410, y=220, width=150)
        Label(self.root, text="Pin", font=("goudy old style", 15, "bold"), bg='white').place(x=580, y=220)
        Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=640, y=220, width=100)

        Label(self.root, text="Address", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=260)

        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), bg='lightblue')
        self.txt_roll.place(x=150, y=60, width=200)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=150, y=100, width=200)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=150, y=140, width=200)
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("SELECT", "MALE", "FEMALE", "OTHER"), font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_gender.place(x=150, y=180, width=200)
        self.txt_gender.current(0)

        # =========col 2======================
        Label(self.root, text="D.O.B", font=("goudy old style", 15, "bold"), bg='white').place(x=360, y=60)
        Label(self.root, text="Contact", font=("goudy old style", 15, "bold"), bg='white').place(x=360, y=100)
        Label(self.root, text="Admission Date", font=("goudy old style", 15, "bold"), bg='white').place(x=360, y=140)
        Label(self.root, text="Course", font=("goudy old style", 15, "bold"), bg='white').place(x=360, y=180)

        self.course_list = []
        self.fetch_course()

        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=520, y=60, width=200)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=520, y=100, width=200)
        Entry(self.root, textvariable=self.var_a_date, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=520, y=140, width=200)

        self.txt_course = ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_course.place(x=520, y=180, width=200)
        self.txt_course.set("Select")

        self.txt_address = Text(self.root, font=("goudy old style", 15, "bold"), bg='lightblue')
        self.txt_address.place(x=150, y=260, width=540, height=100)

        # =====buttons======
        Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="green", fg="white", cursor="hand2", command=self.add).place(x=150, y=400, width=110, height=40)
        Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="purple", fg="white", cursor="hand2", command=self.update).place(x=270, y=400, width=110, height=40)
        Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="red", fg="white", cursor="hand2", command=self.delete).place(x=390, y=400, width=110, height=40)
        Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2", command=self.clear).place(x=510, y=400, width=110, height=40)

        # ====search panel====
        self.var_search = StringVar()
        Label(self.root, text="Roll No.", font=("goudy old style", 15, "bold"), bg='white').place(x=720, y=60)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg='lightblue').place(x=870, y=60, width=180)
        Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="blue", fg="white", cursor="hand2", command=self.Search).place(x=1070, y=60, width=100, height=30)

        # =====content====
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        self.coursetable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"), show='headings', xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.coursetable.xview)
        scrolly.config(command=self.coursetable.yview)
        self.coursetable.pack(fill=BOTH, expand=1)

        for col in self.coursetable["columns"]:
            self.coursetable.heading(col, text=col.capitalize())
            self.coursetable.column(col, width=100)

        self.coursetable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("SELECT")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_a_date.set("")
        self.var_course.set("Select")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.var_search.set("")
        self.txt_address.delete("1.0", END)
        self.txt_roll.config(state=NORMAL)
        self.show()

    def get_data(self, ev=None):
        self.txt_roll.config(state='readonly')
        r = self.coursetable.focus()
        content = self.coursetable.item(r)
        row = content["values"]
        if row:
            self.var_roll.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_dob.set(row[4])
            self.var_contact.set(row[5])
            self.var_a_date.set(row[6])
            self.var_course.set(row[7])
            self.var_state.set(row[8])
            self.var_city.set(row[9])
            self.var_pin.set(row[10])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[11])

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get().strip() == "":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Roll No. already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO student (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_a_date.get(),
                        self.var_course.get(),
                        self.var_state.get(),
                        self.var_city.get(),
                        self.var_pin.get(),
                        self.txt_address.get("1.0", END).strip()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get().strip() == "":
                messagebox.showerror("Error", "Roll No. is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if not row:
                    messagebox.showerror("Error", "Invalid Roll No.", parent=self.root)
                else:
                    cur.execute("UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, state=?, city=?, pin=?, address=? WHERE roll=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_a_date.get(),
                        self.var_course.get(),
                        self.var_state.get(),
                        self.var_city.get(),
                        self.var_pin.get(),
                        self.txt_address.get("1.0", END).strip(),
                        self.var_roll.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            r = self.coursetable.focus()
            content = self.coursetable.item(r)
            row = content["values"]
            if not row:
                messagebox.showerror("Error", "Please select a student", parent=self.root)
                return
            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op:
                cur.execute("DELETE FROM student WHERE roll=?", (row[0],))
                con.commit()
                messagebox.showinfo("Delete", "Deleted successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            self.course_list = [row[0] for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def Search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            roll_no = self.var_search.get().strip()
            if roll_no == "":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=?", (roll_no,))
            rows = cur.fetchall()
            if rows:
                self.coursetable.delete(*self.coursetable.get_children())
                for row in rows:
                    self.coursetable.insert("", END, values=row)
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()
