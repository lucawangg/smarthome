# --------------------------------------------------------------#
# BASE CODE
# --------------------------------------------------------------#
import json
import random

from controller import Robot
from termcolor import cprint

# --------------------------------------------------------------#
# GLOBALS

Compass = 0
Front = 0
FrontLeft = 0
FrontRight = 0
Back = 0
BackLeft = 0
BackRight = 0
Left = 0
Right = 0
CurrentRoom = ""
Rooms = dict()
US_Front = 0
US_Left = 0
US_Right = 0

# --------------------------------------------------------------#
# INIT

robot = Robot()  # Create robot object
timeStep = int(robot.getBasicTimeStep())
maxSpeed = 6.28

wheel_left = robot.getDevice("wheel1 motor")
wheel_left.setPosition(float('inf'))

wheel_right = robot.getDevice("wheel2 motor")
wheel_right.setPosition(float('inf'))

distanceSensor1 = robot.getDevice("D1")
distanceSensor1.enable(timeStep)

distanceSensor2 = robot.getDevice("D2")
distanceSensor2.enable(timeStep)

distanceSensor3 = robot.getDevice("D3")
distanceSensor3.enable(timeStep)

distanceSensor4 = robot.getDevice("D4")
distanceSensor4.enable(timeStep)

distanceSensor5 = robot.getDevice("D5")
distanceSensor5.enable(timeStep)

distanceSensor6 = robot.getDevice("D6")
distanceSensor6.enable(timeStep)

distanceSensor7 = robot.getDevice("D7")
distanceSensor7.enable(timeStep)

distanceSensor8 = robot.getDevice("D8")
distanceSensor8.enable(timeStep)

iuSensor = robot.getDevice("inertial_unit")
iuSensor.enable(timeStep)

receiver = robot.getDevice("receiver")
receiver.setChannel(1)
receiver.enable(timeStep)

# --------------------------------------------------------------#
# TEAM NAME

emitter = robot.getDevice("emitter")
emitter.setChannel(1)
emitter.send('Luca'.encode('utf-8'))

# ---------------------------------------------------------------------------------------------------------------#
# HELPER FUNCTIONS

def rad2deg(rad):
    return (rad / 3.14) * 180


def readSensorsPrimary():
    global Compass, Front, FrontLeft, Left, BackLeft, Back, BackRight, Right, FrontRight
    global US_Front, US_Left, US_Right
    global CurrentRoom, Rooms

    Compass = (rad2deg(iuSensor.getRollPitchYaw()[2]) + 360) % 360
    Front = int(distanceSensor1.getValue() * 10 * 32)
    FrontLeft = int(distanceSensor2.getValue() * 10 * 32)
    Left = int(distanceSensor3.getValue() * 10 * 32)
    BackLeft = int(distanceSensor4.getValue() * 10 * 32)
    Back = int(distanceSensor5.getValue() * 10 * 32)
    BackRight = int(distanceSensor6.getValue() * 10 * 32)
    Right = int(distanceSensor7.getValue() * 10 * 32)
    FrontRight = int(distanceSensor8.getValue() * 10 * 32)
    US_Front = Front
    US_Left = FrontLeft
    US_Right = FrontRight

    if receiver.getQueueLength() > 0:
        received_data = receiver.getString()
        if len(received_data) > 0:
            received_data = json.loads(received_data)
            CurrentRoom = received_data["current_room"]
            room_data = received_data["cleaning_percentage"]
            Rooms = {i['room']: int(float(i["percentage"]) * 100) for i in room_data}
        receiver.nextPacket()

def debugPrimary():
    global Compass, Front, FrontLeft, Back, BackLeft, Back, BackRight, Right, FrontRight
    print()
    cprint("---------------------------------------------", "cyan", )
    cprint("------------------- Debug -------------------", "cyan", )
    cprint("---------------------------------------------", "cyan", )
    print()
    cprint("------------------ Distance -----------------", "yellow", )
    cprint("                       Front: " + str(Front), "yellow")
    cprint("        FrontLeft: " + str(FrontLeft) + "                 FrontRight: " + str(FrontRight), "yellow")
    cprint("Left: " + str(Left) + "                                             Right: " + str(Right), "yellow")
    cprint("        BackLeft: " + str(BackLeft) + "                   BackRight: " + str(BackRight), "yellow")
    cprint("                       Back: " + str(Back), "yellow")
    cprint("------------------- Compass -----------------", "yellow", )
    cprint("Compass: " + str("%.0f " % Compass), "yellow")
    cprint("Current Room: " + CurrentRoom, "yellow")
    cprint("Rooms: " + str.join(", ", map(lambda key: f'{key}: {Rooms[key]}', Rooms.keys())), "yellow")



def move(left, right):
    wheel_left.setVelocity(left * maxSpeed / 10)
    wheel_right.setVelocity(right * maxSpeed / 10)

def eslah(alpha):
    if alpha > 360:
        alpha = alpha - 360
    if alpha < 0:
        alpha = alpha + 360
    return alpha

def turn(deg):
    global Compass
    mindeg = deg-2
    maxdeg = deg+2

    mindeg = eslah(mindeg)
    maxdeg = eslah(maxdeg)

    print(mindeg, deg, maxdeg)
    if(mindeg < maxdeg ):
        if(mindeg < Compass and  Compass < maxdeg):
            return True
    else:
        if(Compass > mindeg or Compass < maxdeg):
            return True
    move (4,-4)
    
    return False


marhale = 0

def jolo():
    global marhale,Front,FrontRight,FrontLeft,duration 
    move(10,10)
    if(FrontLeft < 25 or Front < 25 or FrontRight < 25):
        marhale = marhale + 1
        duration = 0
        
        
def becharkh(deg):
    global marhale
    if turn(deg):
            marhale = marhale + 1



# ---------------------------------------------------------------------------------------------------------------#
# START

global duration
duration = 0
turn_state = 0
A = "Luca Wang"
flag4 = 0
# MAINWHILE

while robot.step(timeStep) != -1:
    readSensorsPrimary()
    debugPrimary()
    #Rooms[CurrentRoom] --> return the cleaning percentage of room the robot is in with type int .
    

    # Start Coding ... 

    if duration > 0:
        duration = duration - 1

    elif turn_state == 1:
        if random.randint(0, 1) == 0:
            move(-5, 10)
        else:
            move(10, -5)

        duration = 11
        turn_state = 0

    elif FrontLeft < 45 and FrontRight < 15:
        move(-5, 10)
        duration = 9
        turn_state = 1

    elif FrontLeft < 43:
        move(-5, 10)
        duration = 12

    elif FrontRight < 43:
        move(10,-5)
        duration = 9
    else:
        left_speed = 8 + random.uniform(-2, 2)
        right_speed = 8 + random.uniform(-2, 2)
        move(left_speed, right_speed)




