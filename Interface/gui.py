import math
import pygame
import pickle
from objects import *
from constants import *
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1400, screen_height))

roads = [
    [[],[],[]],
    [[],[],[]],
    [[],[],[]],
    [[],[],[]]
]

dept = [
    [[],[],[]],
    [[],[],[]],
    [[],[],[]],
    [[],[],[]]
]

car_data = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]


def draw_rect(x, y, width, height, color):
    pygame.draw.rect(screen, color, [x, y, width, height])


def set_traffic_lights(state):
    up_light.state = "off"
    down_light.state = "off"
    left_light.state = "off"
    right_light.state = "off"

    if state == 0:
        left_light.state = "on"
    elif state == 1:
        down_light.state = "on"
    elif state == 2:
        right_light.state = "on"
    elif state == 3:
        up_light.state = "on"


def get_current_state(current_state, traffic_factor, red_timeout, green_time):
    if(green_time < 10):
        return current_state
    for i in range(4):
        if(red_timeout[i] == True):
            return i
    return traffic_factor.index(max(traffic_factor))


run = True

while(run):
    screen.fill(black)
    frames += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    
    # Drawing roads and basics
    draw_rect(0, (screen_height-road_width)/2, screen_width, road_width, black)
    draw_rect((screen_width-road_width)/2, 0, road_width, screen_height, black)
    draw_rect(screen_width/2-1, (screen_height-bar)/2, 2, bar, white)
    draw_rect((screen_width-bar)/2, screen_height/2-1, bar, 2, white)

    ## For up zebra crossing.
    startXX = screen_width/2-road_width
    startXY = (screen_height-road_width)/2 - zebra_distance
    startYX = screen_width/2-road_width
    startYY = (screen_height-road_width)/2 - zebra_distance + zebra_width
    maxX = screen_width/2+road_width
    startXX += zebra_shift
    while(startXX < maxX and startYX < maxX):
        pygame.draw.line(screen, white, (startXX, startXY), (startYX, startYY), 5)
        startXX += 15
        startYX += 15

    ## For down zebra crossing.
    startXX = screen_width/2-road_width
    startXY = (screen_height+road_width)/2 + zebra_distance - zebra_width
    startYX = screen_width/2-road_width
    startYY = (screen_height+road_width)/2 + zebra_distance
    maxX = screen_width/2+road_width
    startXX += zebra_shift
    while(startXX < maxX and startYX < maxX):
        pygame.draw.line(screen, white, (startXX, startXY), (startYX, startYY), 5)
        startXX += 15
        startYX += 15
    
    ## For left zebra crossing.
    startXX = (screen_width-road_width)/2 - zebra_distance
    startXY = screen_height/2-road_width
    startYX = (screen_width-road_width)/2 - zebra_distance + zebra_width
    startYY = screen_height/2-road_width
    maxY = screen_height/2+road_width
    startYY += zebra_shift
    while(startXY < maxY and startYY < maxY):
        pygame.draw.line(screen, white, (startXX, startXY), (startYX, startYY), 5)
        startXY += 15
        startYY += 15

    ## For right zebra crossing.
    startXX = (screen_width+road_width)/2 + zebra_distance - zebra_width
    startXY = screen_height/2-road_width
    startYX = (screen_width+road_width)/2 + zebra_distance
    startYY = screen_height/2-road_width
    maxY = screen_height/2+road_width
    startYY += zebra_shift
    while(startXY < maxY and startYY < maxY):
        pygame.draw.line(screen, white, (startXX, startXY), (startYX, startYY), 5)
        startXY += 15
        startYY += 15
    
    ## For the purple part, outside of the road.
    draw_rect(0, 0, (screen_width-road_width)/2, (screen_height-road_width)/2, grass)
    draw_rect(0, (screen_height+road_width)/2, (screen_width-road_width)/2, (screen_height-road_width)/2, grass)
    draw_rect((screen_width+road_width)/2, 0, (screen_width-road_width)/2, (screen_height-road_width)/2, grass)
    draw_rect((screen_width+road_width)/2, (screen_height+road_width)/2, (screen_width-road_width)/2, (screen_height-road_width)/2, grass)
    
    ## All the lines on the road.
    for i in range(1, 6):
        startX = (screen_width-road_width)/2+i*road_width/6
        startY = 0
        maxY = (screen_height-road_width)/2 - zebra_distance - bar - 3
        while(startY < maxY):
            if(i != 3):
                draw_rect(startX, startY, 1, bar, white)
            else:
                draw_rect(startX, startY, 3, bar, white)
            startY += bar + 15

    for i in range(1, 6):
        startX = (screen_width-road_width)/2+i*road_width/6
        startY = screen_height-bar
        minY = (screen_height+road_width)/2 + zebra_distance
        while(startY > minY):
            if(i != 3):
                draw_rect(startX, startY, 1, bar, white)
            else:
                draw_rect(startX, startY, 3, bar, white)
            startY -= bar + 15

    for i in range(1, 6):
        startX = 0
        startY = (screen_height-road_width)/2+i*road_width/6
        maxX = (screen_width-road_width)/2 - zebra_distance - bar - 3
        while(startX < maxX):
            if(i != 3):
                draw_rect(startX, startY, bar, 1, white)
            else:
                draw_rect(startX, startY, bar, 3, white)
            startX += bar + 15

    for i in range(1, 6):
        startX = screen_width - bar
        startY = (screen_height-road_width)/2+i*road_width/6
        minY = (screen_width+road_width)/2+zebra_distance
        while(startX > minY):
            if(i != 3):
                draw_rect(startX, startY, bar, 1, white)
            else:
                draw_rect(startX, startY, bar, 3, white)
            startX -= bar + 15    
    
    

    # Drawing the lights.
    X = math.floor((screen_width-road_width)/2 - radius - gap)
    Y = math.floor((screen_height+road_width)/2 + radius + gap)
    Xd = math.floor(X-2*radius-gap)
    draw_rect((screen_width-road_width)/2 - 2.5*gap-4*radius, (screen_height+road_width)/2+gap/2, 4*radius+2*gap, 2*radius+gap, grey)
    if(down_light.state is "on"):
        pygame.draw.circle(screen, green, (X, Y), radius)
        pygame.draw.circle(screen, black, (Xd, Y), radius)
    else:
        pygame.draw.circle(screen, black, (X, Y), radius)
        pygame.draw.circle(screen, red, (Xd, Y), radius)

    X = math.floor((screen_width-road_width)/2 - radius - gap)
    Y = math.floor((screen_height-road_width)/2 - radius - gap)
    Yd = math.floor(Y-2*radius-gap)
    draw_rect((screen_width-road_width)/2-1.5*gap-2*radius, (screen_height-road_width)/2-4*radius-2.5*gap, 2*radius+gap, 4*radius+2*gap, grey)
    if(left_light.state is "on"):
        pygame.draw.circle(screen, green, (X, Y), radius)
        pygame.draw.circle(screen, black, (X, Yd), radius)
    else:
        pygame.draw.circle(screen, black, (X, Y), radius)
        pygame.draw.circle(screen, red, (X, Yd), radius)

    X = math.floor((screen_width+road_width)/2 + radius + gap)
    Y = math.floor((screen_height-road_width)/2 - radius - gap)
    Xd = math.floor(X+2*radius+gap)
    draw_rect((screen_width+road_width)/2+0.5*gap, (screen_height-road_width)/2-2*radius-1.5*gap, 4*radius+2*gap, 2*radius+gap, grey)
    if(up_light.state is "on"):
        pygame.draw.circle(screen, green, (X, Y), radius)
        pygame.draw.circle(screen, black, (Xd, Y), radius)
    else:
        pygame.draw.circle(screen, black, (X, Y), radius)
        pygame.draw.circle(screen, red, (Xd, Y), radius)

    X = math.floor((screen_width+road_width)/2 + radius + gap)
    Y = math.floor((screen_height+road_width)/2 + radius + gap)
    Yd = math.floor(Y+2*radius+gap)
    draw_rect((screen_width+road_width)/2+0.5*gap, (screen_height+road_width)/2+0.5*gap, 2*radius+gap, 4*radius+2*gap, grey)
    if(right_light.state is "on"):
        pygame.draw.circle(screen, green, (X, Y), radius)
        pygame.draw.circle(screen, black, (X, Yd), radius)
    else:
        pygame.draw.circle(screen, black, (X, Y), radius)
        pygame.draw.circle(screen, red, (X, Yd), radius)

    with open('traffic_data.pkl', "rb") as f:
        d2 = pickle.load(f)
    for collection in d2:
        if(collection['time'] == frames/100):
            if(collection['lane'] == 0):
                pos = 0
            if(collection['lane'] == 1):
                pos = screen_height
            if(collection['lane'] == 2):
                pos = screen_width
            if(collection['lane'] == 3):
                pos = 0
            vh = vehicle("moving", collection['type'], pos)
            if(len(roads[collection['lane']][collection['sublane']]) <= number):
                roads[collection['lane']][collection['sublane']].append(vh)


    # left to right
    for j in range(3):
        i = 0
        for v in roads[0][j]:
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_left, (v.pos, (screen_height-road_width)/2+5 + j*road_width/6))
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_left, (v.pos, (screen_height-road_width)/2+5 +j*road_width/6))
            if(v.vehicle_type == 'car'):
                screen.blit(car_left, (v.pos, (screen_height-road_width)/2 + j*road_width/6))
            if(j == 0):
                if(all_stop == False):
                    v.pos += speed
                else:
                    if(i > 0):
                        if(roads[0][j][i].pos < roads[0][j][i-1].pos-car_length-speed):
                            v.pos += speed
                    else:
                        if(v.pos < (screen_width-road_width)/2-zebra_distance-car_length-speed or v.pos > (screen_width-road_width)/2-car_length):
                            v.pos += speed
            
            elif(left_light.state == "on"):
                v.pos += speed
            else:
                if(i > 0):
                    if(roads[0][j][i].pos < roads[0][j][i-1].pos-car_length-speed):
                        v.pos += speed
                    else:
                        v.state = "waiting"
                else:
                    if(v.pos < (screen_width-road_width)/2-zebra_distance-car_length-speed or v.pos > (screen_width-road_width)/2-car_length):
                        v.pos += speed
                    else:
                        v.state = "waiting"
            
            i += 1

        for v in dept[0][j]:
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_left, (v.pos, (screen_height-road_width)/2+5 + j*road_width/6))
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_left, (v.pos, (screen_height-road_width)/2+5 +j*road_width/6))
            if(v.vehicle_type == 'car'):
                screen.blit(car_left, (v.pos, (screen_height-road_width)/2 + j*road_width/6))
            v.pos += speed 

    # down to up
    for j in range(3):
        i = 0
        for v in roads[1][j]:
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_down, ((screen_width-road_width)/2+5 + j*road_width/6, v.pos))
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_down, ((screen_width-road_width)/2+5 + j*road_width/6, v.pos))
            if(v.vehicle_type == 'car'):
                screen.blit(car_down, ((screen_width-road_width)/2 + j*road_width/6, v.pos))
            if(j == 0):
                if(all_stop == False):
                    v.pos -= speed
                else:
                    if(i > 0):
                        if(roads[1][j][i].pos > roads[1][j][i-1].pos+car_length+speed):
                            v.pos -= speed
                    else:
                        if(v.pos > (screen_height+road_width)/2+zebra_distance+speed or v.pos < (screen_height+road_width)/2):
                            v.pos -= speed
        
            elif(down_light.state == "on"):
                v.pos -= speed
            else:
                if(i > 0):
                    if(roads[1][j][i].pos > roads[1][j][i-1].pos+car_length+speed):
                        v.pos -= speed
                    else:
                        v.state = "waiting"
                else:
                    if(v.pos > (screen_height+road_width)/2+zebra_distance+speed or v.pos < (screen_height+road_width)/2):
                        v.pos -= speed
                    else:
                        v.state = "waiting"
            
            i += 1

        for v in dept[1][j]:    
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_down, ((screen_width-road_width)/2+5 + j*road_width/6, v.pos))
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_down, ((screen_width-road_width)/2+5 + j*road_width/6, v.pos))
            if(v.vehicle_type == 'car'):
                #print("yo")
                screen.blit(car_down, ((screen_width-road_width)/2 + j*road_width/6, v.pos))
            v.pos -= speed

    # right to left
    for j in range(3):
        i = 0
        for v in roads[2][j]:
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_right, (v.pos, screen_height/2+5 + (2-j)*road_width/6))   
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_right, (v.pos, screen_height/2+5 + (2-j)*road_width/6))
            if(v.vehicle_type == 'car'):
                screen.blit(car_right, (v.pos, screen_height/2 + (2-j)*road_width/6))
            if(j == 0):
                if(all_stop == False):
                    v.pos -= speed
                else:
                    if(i > 0):
                        if(roads[2][j][i].pos > roads[2][j][i-1].pos+car_length+speed):
                            v.pos -= speed
                    else:
                        if(v.pos > (screen_width+road_width)/2+zebra_distance+speed or v.pos < (screen_width+road_width)/2):
                            v.pos -= speed
            
            elif(right_light.state == "on"):
                v.pos -= speed
            else:
                if(i > 0):
                    if(roads[2][j][i].pos > roads[2][j][i-1].pos+car_length+speed):
                        v.pos -= speed
                    else:
                        v.state = "waiting"
                else:
                    if(v.pos > (screen_width+road_width)/2+zebra_distance+speed or v.pos < (screen_width+road_width)/2):
                        v.pos -= speed
                    else:
                        v.state = "waiting"

            i += 1

        for v in dept[2][j]:
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_right, (v.pos, screen_height/2+5 + (2-j)*road_width/6))   
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_right, (v.pos, screen_height/2+5 + (2-j)*road_width/6))
            if(v.vehicle_type == 'car'):
                screen.blit(car_right, (v.pos, screen_height/2 + (2-j)*road_width/6))
            v.pos -= speed
    
    # up to down
    for j in range(3):
        i = 0
        for v in roads[3][j]:
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_up, (screen_width/2+5 + (2-j)*road_width/6, v.pos))               
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_up, (screen_width/2+5 + (2-j)*road_width/6, v.pos))
            if(v.vehicle_type == 'car'):
                screen.blit(car_up, (screen_width/2 + (2-j)*road_width/6, v.pos))
            if(j == 0):
                if(all_stop == False):
                    v.pos += speed
                else:
                    if(i > 0):
                        if(roads[3][j][i].pos < roads[3][j][i-1].pos-car_length-speed):
                            v.pos += speed
                    else:
                        if(v.pos < ((screen_height-road_width)/2-zebra_distance-car_length-speed) or v.pos > (screen_height-road_width)/2-car_length):
                            v.pos += speed

            elif(up_light.state == "on"):
                v.pos += speed
            else:
                if(i > 0):
                    if(roads[3][j][i].pos < roads[3][j][i-1].pos-car_length-speed):
                        v.pos += speed
                    else:
                        v.state = "waiting"
                else:
                    if(v.pos < ((screen_height-road_width)/2-zebra_distance-car_length-speed) or v.pos > (screen_height-road_width)/2-car_length):
                        v.pos += speed

                    else:
                        v.state = "waiting"
            
            i += 1

        for v in dept[3][j]:
            if(v.vehicle_type == 'ambulance'):
                screen.blit(ambulance_up, (screen_width/2+5 + (2-j)*road_width/6, v.pos))               
            if(v.vehicle_type == 'govt_vehicle'):
                screen.blit(govt_up, (screen_width/2+5 + (2-j)*road_width/6, v.pos))
            if(v.vehicle_type == 'car'):
                screen.blit(car_up, (screen_width/2 + (2-j)*road_width/6, v.pos))
            v.pos += speed

    # For left part popping.
    if(len(roads[0][0]) > 0):
        if(roads[0][0][0].pos > (screen_width-road_width)/2):
            vh = roads[0][0].pop(0)
            if(vh.vehicle_type == 'car'):
                vh.pos = (screen_width-road_width)/2
            else:
                vh.pos = (screen_width-road_width)/2+5
            dept[1][0].append(vh)

    if(len(roads[0][1]) > 0):
        if(roads[0][1][0].pos > (screen_width-road_width)/2):
            vh = roads[0][1].pop(0)
            dept[0][1].append(vh)

    if(len(roads[0][2]) > 0):
        if(roads[0][2][0].pos > (screen_width)/2):
            vh = roads[0][2].pop(0)
            if(vh.vehicle_type == 'car'):
                vh.pos = screen_width/2-car_length
            else:
                vh.pos = screen_width/2+5-car_length
            dept[3][2].append(vh)


    # For up part popping.
    if(len(roads[1][0]) > 0):
        if(roads[1][0][0].pos < (screen_height+road_width)/2-car_length):
            vh = roads[1][0].pop(0)
            vh.pos = (screen_width-road_width)/2
            dept[2][0].append(vh)

    if(len(roads[1][1]) > 0):
        if(roads[1][1][0].pos < (screen_height+road_width)/2+zebra_distance):
            vh = roads[1][1].pop(0)
            dept[1][1].append(vh)

    if(len(roads[1][2]) > 0):
        if(roads[1][2][0].pos < (screen_height)/2-car_length):
            vh = roads[1][2].pop(0)
            vh.pos = (screen_width-road_width)/2+road_width/3+5
            dept[0][2].append(vh)

    # For right part popping.
    if(len(roads[2][0]) > 0):
        if(roads[2][0][0].pos < (screen_width+road_width)/2-car_length):
            vh = roads[2][0].pop(0)
            vh.pos = (screen_width+road_width)/2-car_length+5
            dept[3][0].append(vh)

    if(len(roads[2][1]) > 0):
        if(roads[2][1][0].pos < (screen_width+road_width)/2):
            vh = roads[2][1].pop(0)
            dept[2][1].append(vh)

    if(len(roads[2][2]) > 0):
        if(roads[2][2][0].pos < screen_width/2-car_length):
            vh = roads[2][2].pop(0)
            vh.pos = screen_height/2-car_length
            dept[1][2].append(vh)
    
    
    # For down part popping.
    if(len(roads[3][0]) > 0):
        if(roads[3][0][0].pos > (screen_height-road_width)/2):
            vh = roads[3][0].pop(0)
            vh.pos = (screen_width+road_width)/2-car_length
            dept[0][0].append(vh)

    if(len(roads[3][1]) > 0):
        if(roads[3][1][0].pos > (screen_height-road_width)/2):
            vh = roads[3][1].pop(0)
            dept[3][1].append(vh)

    if(len(roads[3][2]) > 0):
        if(roads[3][2][0].pos > (screen_height)/2):
            vh = roads[3][2].pop(0)
            vh.pos = (screen_width)/2-car_length
            dept[2][2].append(vh)
    

    if(frames % 200 == 0):
        all_stop = False
        green_time += 2
        traffic_factor = [0, 0, 0, 0]

        for i in range(4):
            for j in range(1, 3):
                k = 0
                for v in roads[i][j]:
                    if(v.state == "waiting"):
                        v.waiting_time += 2
                        traffic_factor[i] += v.priority * v.waiting_time
                    else:
                        traffic_factor[i] += v.priority
                    k += 1


        for i in range(4):
            if i != current_state:
                stop_time[i] += 2
            if stop_time[i] >= stop_timeout:
                red_timeout[i] = True

        prev_state = current_state

        current_state = get_current_state(current_state, traffic_factor, red_timeout, green_time)
        
        if current_state != prev_state:
            all_stop = True
            stop_time[current_state] = 0
            green_time = 0
            red_timeout[current_state] = False

        if(all_stop == True):
            set_traffic_lights(-1)
        else:
            set_traffic_lights(current_state)

    car_data = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
    
    for i in range(4):
        for j in range(3):
            for v in roads[i][j]:
                if(v.vehicle_type == "car"):
                    car_data[i][0] += 1
                if(v.vehicle_type == "ambulance"):
                    car_data[i][1] += 1
                if(v.vehicle_type == "govt_vehicle"):
                    car_data[i][2] += 1
    
    idx = traffic_factor.index(max(traffic_factor))

    draw_rect(screen_width, 0, 1400-screen_width, screen_height, blue)
    font_size = 30

    text_font = pygame.font.SysFont(None, font_size)
    text = text_font.render("LANE I", True, black)
    screen.blit(text, (40, (screen_height-road_width)/2-text.get_height() - 20))
    
    text = text_font.render("LANE II", True, black)
    text = pygame.transform.rotate(text, 90)
    screen.blit(text, ((screen_width-road_width)/2-text.get_width() - 20, screen_height-40-text.get_height()))

    text = text_font.render("LANE III", True, black)
    screen.blit(text, (screen_width-40-text.get_width(), (screen_height+road_width)/2+20))

    text = text_font.render("LANE IV", True, black)
    text = pygame.transform.rotate(text, 270)
    screen.blit(text, ((screen_width+road_width)/2+text.get_width(), 40))

    text_font = pygame.font.Font("freesansbold.ttf", 40)
    text = text_font.render("LANE I :", True, white)
    text_font = pygame.font.Font("freesansbold.ttf", font_size)
    screen.blit(text, (screen_width+30, 70))
    text = text_font.render("Normal : " + str(car_data[0][0]), True, white)
    screen.blit(text, (screen_width+30, 110))
    text = text_font.render("Ambulance : " + str(car_data[0][1]), True, white)
    screen.blit(text, (screen_width+30, 150))
    text = text_font.render("Govt owned vehicle : " + str(car_data[0][2]), True, white)
    screen.blit(text, (screen_width+30, 190))
    if(idx == 0):
        text = text_font.render("Traffic factor : " + str(traffic_factor[0]), True, red)
    else:
        text = text_font.render("Traffic factor : " + str(traffic_factor[0]), True, white)
    screen.blit(text, (screen_width+30, 230))

    text_font = pygame.font.Font("freesansbold.ttf", 40)
    text = text_font.render("LANE II :", True, white)
    text_font = pygame.font.Font("freesansbold.ttf", font_size)
    screen.blit(text, (screen_width+30, 290))
    text = text_font.render("Normal : " + str(car_data[1][0]), True, white)
    screen.blit(text, (screen_width+30, 330))
    text = text_font.render("Ambulance : " + str(car_data[1][1]), True, white)
    screen.blit(text, (screen_width+30, 370))
    text = text_font.render("Govt owned vehicle : " + str(car_data[1][2]), True, white)
    screen.blit(text, (screen_width+30, 410))
    if(idx == 1):
        text = text_font.render("Traffic factor : " + str(traffic_factor[1]), True, red)
    else:
        text = text_font.render("Traffic factor : " + str(traffic_factor[1]), True, white)
    screen.blit(text, (screen_width+30, 450))

    text_font = pygame.font.Font("freesansbold.ttf", 40)
    text = text_font.render("LANE III :", True, white)
    text_font = pygame.font.Font("freesansbold.ttf", font_size)
    screen.blit(text, (screen_width+30, 510))
    text = text_font.render("Normal : " + str(car_data[2][0]), True, white)
    screen.blit(text, (screen_width+30, 560))
    text = text_font.render("Ambulance : " + str(car_data[2][1]), True, white)
    screen.blit(text, (screen_width+30, 600))
    text = text_font.render("Govt owned vehicle : " + str(car_data[2][2]), True, white)
    screen.blit(text, (screen_width+30, 640))
    if(idx == 2):
        text = text_font.render("Traffic factor : " + str(traffic_factor[2]), True, red)
    else:
        text = text_font.render("Traffic factor : " + str(traffic_factor[2]), True, white)
    screen.blit(text, (screen_width+30, 680))

    text_font = pygame.font.Font("freesansbold.ttf", 40)
    text = text_font.render("LANE IV :", True, white)
    text_font = pygame.font.Font("freesansbold.ttf", font_size)
    screen.blit(text, (screen_width+30, 740))
    text = text_font.render("Normal : " + str(car_data[3][0]), True, white)
    screen.blit(text, (screen_width+30, 780))
    text = text_font.render("Ambulance : " + str(car_data[3][1]), True, white)
    screen.blit(text, (screen_width+30, 820))
    text = text_font.render("Govt owned vehicle : " + str(car_data[3][2]), True, white)
    screen.blit(text, (screen_width+30, 860))
    if(idx == 3):
        text = text_font.render("Traffic factor : " + str(traffic_factor[3]), True, red)
    else:
        text = text_font.render("Traffic factor : " + str(traffic_factor[3]), True, white)
    screen.blit(text, (screen_width+30, 900))
    
    frames = frames%4000

    clock.tick(100)
    pygame.display.update()
