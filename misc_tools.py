from random import uniform

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

def compute_intersection(seg1, seg2):

    A = seg1[0]
    B = seg1[1]

    C = seg2[0]
    D = seg2[1]

    E = (B[0]-A[0],B[1]-A[1])
    F = (D[0]-C[0],D[1]-C[1])

    cross_e_f = cross_prod(E,F)

    if cross_e_f == 0:
        return None

    c_min_a = (C[0]-A[0],C[1]-A[1])

    t = cross_prod(c_min_a,F)/cross_e_f
    u = cross_prod(c_min_a,E)/cross_e_f

    if not (t >= 0 and t <= 1 and u >= 0 and u <= 1):
        return None

    intersect = (A[0] + t*E[0], A[1] + t*E[1])
    intersect = (intersect[0], round(intersect[1], 6))

    return intersect

def cross_prod(a, b):

    # since the points are 2D, the cross product is trivial
    return a[0]*b[1] - b[0]*a[1]

def compute_slope(a,b):
    return (a[1]-b[1])/(a[0]-b[0])