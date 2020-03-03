import random
import pickle

freq = {'High': 6, 'Low': 10}
lane_freq = ['High', 'Low', 'High', 'Low']
vehicle_types = ['car', 'ambulance', 'govt_vehicle']
data = []

for lane in range(4):
    for sublane in range(3):
        time = 0
        for i in range(5):
            delay = random.randint(1,freq[lane_freq[lane]])
            time += delay
            v = random.choices(vehicle_types, [0.9, 0.07, 0.03])[0]
            data.append({'lane': lane, 'sublane': sublane, 'time': time, 'type': v})

with open('traffic_data.pkl', "wb") as f:
    pickle.dump(data, f)
