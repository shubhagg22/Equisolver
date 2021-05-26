from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw
from run_model import out_answer

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        
        self.root.title('EquiSolver')
        self.ico = Image.open('equi-logo.ico')
        self.ico = ImageTk.PhotoImage(self.ico)
        self.root.wm_iconphoto(False, self.ico)
        self.pen_button = Button(self.root, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0, padx=50,pady=10,ipadx=50)

        self.color_button = Button(self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=1,padx=50,pady=10,ipadx=50)

        self.reset_button = Button(self.root, text='Reset', command=self.reset)
        self.reset_button.grid(row=0, column=2,padx=50,pady=10,ipadx=50)

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3,padx=50,pady=10,ipadx=50)

        self.solve_button = Button(self.root, text='Solve', command=self.solve)
        self.solve_button.grid(row=0, column=4, padx=50,pady=10,ipadx=50)

        self.inputarg=StringVar()
        self.inputarg.set('Result')
        self.in_lab=Label(self.root,textvariable=self.inputarg)
        self.in_lab.grid(row=1,column=2)

        self.output=StringVar()
        self.output.set('')
        self.out_lab=Label(self.root,textvariable=self.output)
        self.out_lab.grid(row=2,column=2)
        
        self.c = Canvas(self.root, bg='white', width=1000, height=600)
        self.c.grid(row=3, columnspan=8)

        self.image1=Image.new("RGB",(1000,600),'white')
        self.draw=ImageDraw.Draw(self.image1)
        
        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset_pos)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = 20 if self.eraser_on else 5
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND,smooth=TRUE)
            self.draw.line([self.old_x, self.old_y, event.x, event.y],
                           width=self.line_width, fill=paint_color,
                           joint='curve')
        self.old_x = event.x
        self.old_y = event.y

    def reset_pos(self,event):
        self.old_x, self.old_y = None, None

    def reset(self):
        self.color=self.DEFAULT_COLOR
        self.c.create_rectangle(0,0,1010,610,fill='white')
        self.draw.rectangle([0,0,1010,610,],fill='white')
    
    def solve(self):
        self.inputarg.set("Result")
        self.output.set("")
        fileName='save.png'
        self.image1.save(fileName)
        out=out_answer(fileName)
        if out==False:
            return
        if "=" not in out[0]:
            self.inputarg.set(out[0]+"="+out[1])
        else:
            self.inputarg.set(out[0])
            self.output.set(out[1])

if __name__ == '__main__':
    Paint()
