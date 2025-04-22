from tkinter import *
from PIL import Image, ImageTk  # For handling images (if used)
from tkinter import ttk, messagebox
import sqlite3

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ===== Title =====
        title = Label(self.root, text="View Student Result", font=("goudy old style", 20, "bold"),
                      bg="orange", fg="#262626")
        title.place(x=10, y=15, width=1180, height=50)

        # ===== Search Area =====
        self.var_search = StringVar()
        self.var_id = ""  # Used internally to hold the result ID from database

        lbl_search = Label(self.root, text="Search By Roll No", font=("goudy old style", 20, "bold"), bg="white")
        lbl_search.place(x=350, y=100)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 20), bg="lightyellow")
        txt_search.place(x=520, y=100, width=150)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="blue", fg="white",
                            cursor="hand2", command=self.search)
        btn_search.place(x=680, y=100, width=120, height=35)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="gray", fg="white",
                           cursor="hand2", command=self.clear)
        btn_clear.place(x=820, y=100, width=100, height=35)

        # ===== Labels for Result Display Headings =====
        headings = [("Roll No", 150), ("Name", 300), ("Course", 450), ("Marks Obtained", 600),
                    ("Total Marks", 750), ("Percentage", 900)]
        for text, x in headings:
            Label(self.root, text=text, font=("goudy old style", 15, "bold"), bg="white",
                  bd=2, relief=GROOVE).place(x=x, y=230, width=150, height=50)

        # ===== Labels to Display Search Result =====
        self.roll = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.roll.place(x=150, y=280, width=150, height=50)
        self.name = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.name.place(x=300, y=280, width=150, height=50)
        self.course = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.course.place(x=450, y=280, width=150, height=50)
        self.marks = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.marks.place(x=600, y=280, width=150, height=50)
        self.full = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.full.place(x=750, y=280, width=150, height=50)
        self.per = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.per.place(x=900, y=280, width=150, height=50)

        # ===== Delete Button =====
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="red", fg="white",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=500, y=350, width=150, height=35)

    # ===== Search Function =====
    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll No. is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE roll=?", (self.var_search.get(),))
                row = cur.fetchone()
                if row:
                    self.var_id = row[0]
                    self.roll.config(text=row[1])
                    self.name.config(text=row[2])
                    self.course.config(text=row[3])
                    self.marks.config(text=row[4])
                    self.full.config(text=row[5])
                    self.per.config(text=row[6])
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # ===== Clear Function =====
    def clear(self):
        self.var_id = ""
        self.var_search.set("")
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")

    # ===== Delete Function =====
    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_id == "":
                messagebox.showerror("Error", "Search student result first", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE rid=?", (self.var_id,))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid student result", parent=self.root)
                else:
                    confirm = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if confirm:
                        cur.execute("DELETE FROM result WHERE rid=?", (self.var_id,))
                        con.commit()
                        messagebox.showinfo("Deleted", "Result deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

# ===== Main =====
if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()
