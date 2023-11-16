from RedBlackTree import *
from misc_tools import generate_rand_segments
from bentley_ottmann import bentley_ottmann
from datetime import datetime
from tkinter import *


YSIZE = 1000
PSIZE = 4

def drawSegments(S):
    for s in S:
        drawLine(s[0], s[1], 'black')

def drawLine(p1, p2, color):
    p1 = (p1[0], YSIZE - p1[1])
    p2 = (p2[0], YSIZE - p2[1])
    canvas.create_line(p1, p2, fill=color)

def drawPoint(point):
    p = (point[0], YSIZE - point[1])
    canvas.create_oval(p[0] - PSIZE, p[1] - PSIZE, p[0] + PSIZE, p[1] + PSIZE, fill='red', w=2)

# =========================================
root = Tk()
root.title("Segments")
root.geometry(str(YSIZE)+'x'+str(YSIZE)) #("800x800")

canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.grid(row=0, column=0)

while True:

    S = generate_rand_segments(200)

    BOTime = datetime.now()
    points = bentley_ottmann(S)
    BOTime = datetime.now() - BOTime

    # not valid set of segments
    if points == -1:
        continue

    print(S)
    print(points)
    drawSegments(S)
    for point in points:
        drawPoint(point)
    print("number of intersections found:", len(points), "time taken:", BOTime)
    break

root.mainloop()
