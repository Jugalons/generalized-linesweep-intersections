from RedBlackTree import *
from functools import cmp_to_key
from random import uniform
from bentley_ottmann import bentley_ottmann
from datetime import datetime
from tkinter import *


YSIZE = 1000
PSIZE = 4

#-----------------------------------------------------------------
# Event class for endpts and intersection pts in our event queue
#-----------------------------------------------------------------
class Event:
    def __init__(self, x, y, is_left=True, is_intersection=False, other_end=None, label=None, pl=None, ps=None, sl = None, ss=None):
        self.x = x
        self.y = y
        self.is_left = is_left
        self.is_intersection = is_intersection
        self.other_end = other_end
        self.label = label
        # fields for intersection events
        self.plabel=pl
        self.psegment=ps
        self.slabel=sl
        self.ssegment=ss


    def __str__(self):
        return str(self.label) + ' ' + str(self.plabel) + ' ' + str(self.slabel)


#-----------------------------------------------------------------
# find_intersections callback
#-----------------------------------------------------------------
def find_intersections(event):
    global S
    Q = RedBlackTree()
    label = 0
    for s in S:
        if s[0][0] > s[1][0]:
            S[label] = (s[1],s[0])
            s = S[label]
        Q.insert(s[0][0], Event(s[0][0], s[0][1], True, False, s[1], label))
        Q.insert(s[1][0], Event(s[1][0], s[1][1], False, False, s[0], label))
        label += 1
  
    T = RedBlackTree()
    
    intersections = []
    
    while not Q.is_empty():
        min_node = Q.minimum()
        event = min_node.data
        Q.delete(min_node)
        if event.is_left:
            print("left event")
	    # *** need to implement ***

        elif not event.is_intersection:
            print("right event")
	    # *** need to implement ***

        else:
            print("intersection event")
	    # *** need to implement ***
          
    print(intersections)


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

def generate_rand_segments(n):
    
    points = list()
    
    while n > 0:
        
        seg = [(round(uniform(100,900),6),round(uniform(300,900),6)),(round(uniform(100,900),6),round(uniform(300,900),6))]

        # cannot have vertical segments
        if seg[0][1] == seg[1][1]:
            continue

        points.append(seg)

        n = n-1

    return points

# =========================================
root = Tk()
root.title("Segments")
root.geometry(str(YSIZE)+'x'+str(YSIZE)) #("800x800")

canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", find_intersections)
canvas.grid(row=0, column=0)

while True:

    S = generate_rand_segments(10)


    
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
