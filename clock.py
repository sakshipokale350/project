from tkinter import*
from PIL import Image,ImageTk,ImageDraw #pip install pillow
from datetime import*
import time
from math import *


class Clock:
    def __init__(self,root):
        self.root=root
        self.root.title("GUI Analog clock")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#022e2f")



        title=Label(self.root,text="Webcode Analog Clock",font=("times new roman",50,"bold"),bg="#05555a",fg="white").place(x=0,y=50,relwidth=1) 

        self.lbl=Label(self.root,bg="white",bd=10,relief=RAISED)
        self.lbl.place(x=450, y=150, height=400, width=400)
        self.working()

    def clock_image(self,hr,min_,sec_):
        clock_image = Image.new("RGB", (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(clock_image)
# =====this is clock images : basic structure ===========================   
        bg = Image.open("images/cl.jpg")
        bg = bg.resize((300, 300), Image.LANCZOS)
        clock_image.paste(bg, (50, 50))
        clock_image.save("clock_new.png")

# =========================formula to rotate the clock==================
        # angle_in_radian=angle_in_degress * math.pi /180
        # line_length=100
        # center_x=250
        # centre_y=250
        # end_x=center_x + line_length * math.cos(angle_in_radians)
        # end_y=centre_y + line_length * math.sin(angle_in_radians)


 #======= hours===create a line inside the clock================================

#               x1,y1,x2,x2

        origin=200,200
        draw.line((origin,200+50*sin(radians(hr)),200-50*cos(radians(hr))),fill="black",width=4)
 #== min=====create a line inside the clock ================================
        draw.line((origin,200+80*sin(radians(min_)),200-80*cos(radians(min_))),fill="blue",width=3)

 #===second====create a line inside the clock================================
        draw.line((origin,200+100*sin(radians(sec_)),200-100*cos(radians(sec_))),fill="green",width=4)

 # ======draw a circle =============
        draw.ellipse((195,195,210,210),fill="black")             
        clock_image.save("clock_new.png")
#


# =========create a function for working of clock========import module datetime
    def working(self):
        h=datetime.now().time().hour
        m=datetime.now().time().minute
        s=datetime.now().time().second
        # print(h,m,s)
#=========create an angles ========        
        hr=(h/12)*360
        min_=(m/60)*360
        sec_=(s/60)*360
        # print(hr,min_,sec_)
        self.clock_image(hr,min_,sec_)
        self.img=ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200,self.working)







root=Tk()
obj=Clock(root)
root.mainloop()   