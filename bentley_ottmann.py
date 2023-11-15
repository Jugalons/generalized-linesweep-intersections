from misc_tools import compute_intersection
from EventData import EventData
from SweepData import SweepData
from RedBlackTree import RedBlackTree

# The bentley-ottmann algorithm solves the 2D segment intersect
# problem in time complexity O(nlog(n)).
def bentley_ottmann(S):

    Q = RedBlackTree()
    T = RedBlackTree()
    I = list()

    for segment in S:
        # sorted on the segment's endpoints x values
        segment = sorted(segment)

        # both insertion and remove events for a segment need a reference
        # to the key of its sweep line node
        sweep_key = segment[0][1]

        # set insert segment event key to minimum x coordinate
        event_key = segment[0][0]
        size_before = Q.size
        Q.insert(event_key, EventData(insert_segment, segment, sweep_key, event_key))
        if size_before == Q.size:
            print("unable to properly insert a line segment into event queue")
            return -1

        # set remove segment event key to maximum x coordinate
        event_key = segment[1][0]
        size_before = Q.size
        Q.insert(event_key, EventData(remove_segment, segment, sweep_key, event_key))
        if size_before == Q.size:
            print("unable to properly insert segment into queue")
            return -1

    # get the event nodes in order
    for node in Q.inorder():
        if process_event(T, I, Q, node) == -1:
            return -1
        Q.delete(node)
    
    if not T.is_empty or not Q.is_empty:
        print("yo your shit ain't working! >:(")

    return I

def process_event(T, I, Q, node):

    # the data of a node is the event object
    event = node.data

    # executing the event handlers (see functions below)
    if event.execute == intersection:
        if event.execute(T, Q, I, event) == -1:
            return -1
    else:
        if event.execute(T, Q, event) == -1:
            return -1

def intersection(T, Q, I, event_data):

    # add intersection point to set of intersections
    I.append(event_data.intersect)

    # swap the two segments in sweep tree
    #   need to swap the data of the segments in sweep line and update the
    #   keys in queue for remove events of each segment
    event_y = event_data.intersect[1]
    node1 = T.sweep_search(event_y, event_data.event_key)
    if node1.key == event_data.sweep_key:
        node2 = T.successor(node1)
    else:
        node2 = node1
        node1 = T.predecessor(node2)

    node1_key = node1.key
    node2_key = node2.key

    # update the remove event(s) sweep keys
    update_remove_event(Q, node1.data.event_key, node2_key)
    update_remove_event(Q, node2.data.event_key, node1_key)

    # perform the swap
    data = node1.data
    node1.data = node2.data
    node2.data = data

    # check for intersection(s) between unseen neighbors
    node_pred = node1
    node_succ = node2
    pred = T.predecessor(node_pred)
    succ = T.successor(node_succ)

    if pred:
        if add_intersection(Q, event_data.event_key, pred.data.segment, pred.key, node_pred.data.segment, node_pred.key) == -1:
            return -1
    if succ:
        if add_intersection(Q, event_data.event_key, node_succ.data.segment, node_succ.key, succ.data.segment, succ.key) == -1:
            return -1

def insert_segment(T, Q, event_data):

    size_before = T.size
    # insert the line segment into line sweep tree
    # using the event key, or the x value of the left-most point of segment 'seg'
    # we may insert a sweep_key, or the y value of the left-most point segment 'seg',
    # into the line sweep tree.
    sweep_node = T.insert(event_data.sweep_key, SweepData(event_data.segment))
    
    # check for degenerate case
    if T.size == size_before:
        print("unable to insert segment", event_data.segment, "into sweep line")
        return -1

    pred = T.predecessor(sweep_node)
    succ = T.successor(sweep_node)

    # remove an intersection between predecessor and successor
    if pred and succ:
        intersect = compute_intersection(pred.data.segment,succ.data.segment)
        if(not intersect is None):
            event_key = intersect[0]
            if event_data.event_key < event_key:
                intersect_event = Q.search(event_key)
                Q.delete(intersect_event)

    # update the keys of predecessor and successor
    # add new intersection event(s) to queue
    if pred:
        if add_intersection(Q, event_data.event_key, pred.data.segment, pred.key, sweep_node.data.segment, sweep_node.key) == -1:
            return -1
    if succ:
        if add_intersection(Q, event_data.event_key, sweep_node.data.segment, sweep_node.key, succ.data.segment, succ.key) == -1:
            return -1

def remove_segment(T, Q, event_data):

    event_y = event_data.segment[1][1]
    node = T.sweep_search(event_y, event_data.event_key)
    pred = T.predecessor(node)
    succ = T.successor(node)

    # add an intersection between predecessor and successor to event queue
    if pred and succ:
        add_intersection(Q, event_data.event_key, pred.data.segment, pred.key, succ.data.segment, succ.key)

    # remove the node from sweep line
    T.delete(node)

def update_remove_event(Q, event_key, sweep_key):
    end_event = Q.search(event_key)
    end_event.data.sweep_key = sweep_key
    return end_event

def add_intersection(Q, curr_event_key, seg1, key1, seg2, key2):
    intersect = compute_intersection(seg1, seg2)
    if(not intersect is None):

        event_key = intersect[0]

        # do not resolve past intersections
        if curr_event_key > event_key:
            return

        node = Q.search(event_key)

        # intersection DNE ==> first time addition
        if node.key is None:
            Q.insert(event_key, EventData(intersection, seg1, key1, event_key, seg2, key2, intersect))
        else:
            # intersection node exists between two other segments == cannot insert intersection
            if(not ((seg1 == node.data.segment or seg1 == node.data.segment_two) and (seg2 == node.data.segment or seg2 == node.data.segment_two))):
                print("cannot insert intersection into the queue")
                return -1
        
            # simply modify existing intersection node with correct sweep keys
            node.data.sweep_key = key1
            node.data.sweep_key_two = key2