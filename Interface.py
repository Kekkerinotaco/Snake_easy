# Creating the interface

from tkinter import *

window = Tk()
window.title("KrasNIPI in collaboration with GPN snake game for $1000000000")

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True

c = Canvas(window, width=WIDTH, height=HEIGHT, bg="#555555")
c.grid()
c.focus_set()
window.mainloop()
