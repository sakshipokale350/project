from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3


class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====== Title ======
        title = Label(self.root, text="Manage Course Details", font=("goudy old style", 20, "bold"),
                      bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # ===== Variables =====
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        # ===== Labels =====
        Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=60)
        Label(self.root, text="Duration", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=100)
        Label(self.root, text="Charges", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=140)
        Label(self.root, text="Description", font=("goudy old style", 15, "bold"), bg='white').place(x=10, y=180)

        # ===== Entry Fields =====
        self.txt_coursename = Entry(self.root, textvariable=self.var_course,
                                    font=("goudy old style", 15), bg='lightyellow')
        self.txt_coursename.place(x=150, y=60, width=200)

        Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=100, width=200)
        Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15), bg='lightyellow').place(x=150, y=140, width=200)

        self.txt_description = Text(self.root, font=("goudy old style", 15), bg='lightyellow')
        self.txt_description.place(x=150, y=180, width=500, height=140)

        # ===== Buttons =====
        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15, "bold"),
               bg="green", fg="white", cursor="hand2").place(x=150, y=400, width=110, height=40)

        Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"),
               bg="purple", fg="white", cursor="hand2").place(x=270, y=400, width=110, height=40)

        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"),
               bg="red", fg="white", cursor="hand2").place(x=390, y=400, width=110, height=40)

        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"),
               bg="gray", fg="white", cursor="hand2").place(x=510, y=400, width=110, height=40)

        # ===== Search Panel =====
        Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg='white').place(x=720, y=60)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15), bg='lightyellow').place(x=870, y=60, width=180)
        Button(self.root, text="Search", command=self.search, font=("goudy old style", 15),
               bg="blue", fg="white", cursor="hand2").place(x=1070, y=60, width=120, height=28)

        # ===== Treeview Frame =====
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.coursetable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"),
                                        yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.coursetable.xview)
        scrolly.config(command=self.coursetable.yview)

        self.coursetable.heading("cid", text="Course ID")
        self.coursetable.heading("name", text="Name")
        self.coursetable.heading("duration", text="Duration")
        self.coursetable.heading("charges", text="Charges")
        self.coursetable.heading("description", text="Description")
        self.coursetable["show"] = "headings"

        self.coursetable.column("cid", width=50)
        self.coursetable.column("name", width=100)
        self.coursetable.column("duration", width=100)
        self.coursetable.column("charges", width=100)
        self.coursetable.column("description", width=150)

        self.coursetable.pack(fill=BOTH, expand=1)
        self.coursetable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ===== Functions =====
    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_coursename.config(state=NORMAL)
        self.show()

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Course Name already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END).strip()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if not row:
                    messagebox.showerror("Error", "Select course from list", parent=self.root)
                else:
                    cur.execute("UPDATE course SET duration=?, charges=?, description=? WHERE name=?", (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END).strip(),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if not row:
                    messagebox.showerror("Error", "Please select course from the list", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM course WHERE name=?", (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Course deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        self.txt_coursename.config(state='readonly')
        selected = self.coursetable.focus()
        content = self.coursetable.item(selected)
        row = content["values"]
        if row:
            self.var_course.set(row[1])
            self.var_duration.set(row[2])
            self.var_charges.set(row[3])
            self.txt_description.delete("1.0", END)
            self.txt_description.insert(END, row[4])

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
            rows = cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
