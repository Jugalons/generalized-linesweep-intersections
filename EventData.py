class EventData:
    def __init__(self, event_handler, segment, sweep_key, event_key, segment_two=None, sweep_key_two=None, intersect=None):
        # event data fields
        self.execute = event_handler
        self.segment = segment
        self.sweep_key = sweep_key
        self.event_key = event_key

        # additional intersect event fields
        self.segment_two = segment_two
        self.sweep_key_two = sweep_key_two
        self.intersect = intersect
    
    # returns the event key
    def compute_adjusted_key(self, x):
        return self.event_key

    