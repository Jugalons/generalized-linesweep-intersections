from misc_tools import compute_slope

class SweepData:

    def __init__(self, seg):
        # data fields
        self.m = compute_slope(seg[0], seg[1])
        self.b = seg[0][1] - self.m*seg[0][0] # y = mx + b => b = y - m*x for some (x,y)
        self.event_key = seg[1][0]
        self.segment = seg
    
    def compute_adjusted_key(self, x):
        val = self.m*x + self.b
        return round(val, 6)

