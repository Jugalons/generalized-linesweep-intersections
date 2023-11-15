from bentley_ottmann import bentley_ottmann, intersection
from misc_tools import generate_rand_segments
from datetime import datetime
import sys

sys.stdout = open('output.txt', 'w')


test_one = False
test_two = False
test_three = False
test_four = False
test_five = False
test_six = False
test_seven = False
test_eight = False
test_nine = False
test_ten = False

while True:

    S = generate_rand_segments(200)

    try:
        BOTime = datetime.now()
        points = bentley_ottmann(S)
        BOTime = datetime.now() - BOTime
    except:
        continue

    # not valid set of segments
    if points == -1:
        continue

    intersections = len(points)

    if intersections <= 3000 and not test_one:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_one = True
    elif intersections >= 3000 and not test_two:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_two = True
    elif intersections >= 5000 and not test_three:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_three = True
    elif intersections >= 6000 and not test_four:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_four = True
    elif intersections >= 7000 and not test_five:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_five = True
    elif intersections >= 8000 and not test_six:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_six = True
    elif intersections >= 9000 and not test_seven:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_seven = True
    elif intersections >= 10000 and not test_eight:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_eight = True
    elif intersections >= 12000 and not test_nine:
        sys.stdout.write("number of intersections found: " + str(len(points)) + " time taken:" + str(BOTime) + '\n')
        sys.stdout.write("Set of points: \n" + str(S) + '\n')
        test_nine = True    

    if test_one and test_two and test_three and test_four and test_five and test_six and test_seven and test_eight and test_nine and test_ten:
        break