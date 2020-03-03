class vehicle():
    def __init__(self, state, vehicle_type, pos):
        self.state = state
        self.vehicle_type = vehicle_type
        self.priority = self.get_priority(vehicle_type)
        self.waiting_time = 0
        self.pos = pos

    def get_priority(self, vehicle_type):
        if(vehicle_type == "car"):
            return 1
        elif(vehicle_type == "govt_vehicle"):
            return 100
        elif(vehicle_type == "ambulance"):
            return 1000
        else:
            return -1

class lights():
    def __init__(self):
        self.max_red = 150
        self.min_green = 10
        self.state = "off"

