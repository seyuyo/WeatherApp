from tkinter import Tk, Canvas

root = Tk()
canvas = Canvas(root, width=200, height=200)
canvas.pack()

# Lekerekített négyzet rajzolása
x1, y1 = 50, 50
x2, y2 = 150, 150
radius = 10

canvas.create_arc(x1, y1, x1+2*radius, y1+2*radius, start=90, extent=90,
                  outline='black', fill='black', width=2, style='pieslice')
canvas.create_arc(x2-2*radius, y1, x2, y1+2*radius, start=0, extent=90,
                  outline='black', fill='black', width=2, style='pieslice')
canvas.create_arc(x1, y2-2*radius, x1+2*radius, y2, start=180, extent=90,
                  outline='black', fill='black', width=2, style='pieslice')
canvas.create_arc(x2-2*radius, y2-2*radius, x2, y2, start=270, extent=90,
                  outline='black', fill='black', width=2, style='pieslice')

root.mainloop()


"""
from tkinter import Tk, Canvas

root = Tk()
canvas = Canvas(root, width=200, height=200)
canvas.pack()

# Lekerekített négyzet rajzolása
x1, y1 = 50, 50
x2, y2 = 150, 150
radius = 10

canvas.create_polygon(x1+radius, y1, x2-radius, y1, x2, y1+radius, x2, y2-radius, 
                      x2-radius, y2, x1+radius, y2, x1, y2-radius, x1, y1+radius, 
                      outline='black', fill='black')

root.mainloop()

"""