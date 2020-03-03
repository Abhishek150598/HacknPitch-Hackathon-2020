import pygame
from objects import *

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
light_green = (0, 200, 100)
magenta = (128, 0, 128)
green = (76, 153, 0)
red = (255, 0, 0)
yellow = (205, 205, 0)
blue = (0, 0, 51)
#grass = (0, 153, 0)
grass = light_green
grey = (60, 60, 60)

# Setting the display
screen_width = 1000
screen_height = 1000

# System Constants
road_width = 240
zebra_width = 30
zebra_distance = 50
zebra_shift = 10
bar = 50
radius = 15
gap = 10
car_length = 40
car_width = road_width/6-10
speed = 2
frames = 0

current_state = 0
prev_state = 1
stop_time = [0, 0, 0, 0]
red_timeout = [False, False, False, False]
green_time = 0
all_stop = False
traffic_factor = [0, 0, 0, 0]
number = int(((screen_height-road_width)/2-zebra_distance)/(car_length+speed))

# Loading all images.
car = pygame.image.load('car.png')
car = pygame.transform.rotate(car, 90)
car_right = pygame.transform.scale(car, (int(car_length), int(car_width+10)))
car_left = pygame.transform.rotate(car_right, 180)
car_up = pygame.transform.rotate(car_right, 90)
car_down = pygame.transform.rotate(car_left, 90)

ambulance = pygame.image.load('ambulance.png')
ambulance = pygame.transform.rotate(ambulance, 90)
ambulance_right = pygame.transform.scale(ambulance, (int(car_length), int(car_width)))
ambulance_left = pygame.transform.rotate(ambulance_right, 180)
ambulance_up = pygame.transform.rotate(ambulance_right, 90)
ambulance_down = pygame.transform.rotate(ambulance_left, 90)

govt = pygame.image.load('govt.png')
govt_right = pygame.transform.scale(govt, (int(car_length), int(car_width)))
govt_left = pygame.transform.rotate(govt_right, 180)
govt_up = pygame.transform.rotate(govt_right, 90)
govt_down = pygame.transform.rotate(govt_left, 90)


# All the lights.
up_light = lights()
down_light = lights()
left_light = lights()
right_light = lights()

stop_timeout = 100