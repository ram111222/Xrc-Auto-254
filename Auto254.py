from simple_pid import PID
import math


#Define variables
xPositions = 0
YPositions = 0
rRotation = 0
positionList = [xPositions,YPositions,rRotation]
xTarget = 0
yTarget = 0
rTarget = 0
targetList = [xTarget,yTarget,rTarget]
xMove = 0
yMove = 0
rMove = 0
moveList = [xMove,yMove,rMove]

PATH = "C:\\tmp\\xRCsim\\"
inputs = {
    "a": 0,
    "b": 0,
    "x": 0,
    "y": 0,
    "dpad_down": 0,
    "dpad_up": 0,
    "dpad_left": 0,
    "dpad_right": 0,
    "bumper_l": 0,
    "bumper_r": 0,
    "stop": 0,
    "restart": 0,
    "right_y": 0,
    "right_x": 0,
    "left_y": 0,
    "left_x": 0,
    "trigger_l": 0,
    "trigger_r": 0,
    }

#Define PID
Rpid  = PID(-0.005,-0.0,-0.0,setpoint=0.0,output_limits = (-1,1))
Xpid = PID(-0.3,-0.0,-0.01,setpoint=0.0,output_limits = (-1,1))
Ypid = PID(-0.3,-0.0,-0.05,setpoint=0.0,output_limits = (-1,1))

def getRobotPosition():
    while True:
        RBot = open('C:\\tmp\\xRCsim\\myRobot.txt',"rt")
        Robot = RBot.readlines()
        try:
            xPositions = float(Robot[10].removeprefix('\t\t\t"global pos":[').removesuffix("],\n").split(",")[0])
            YPositions = float(Robot[10].removeprefix('\t\t\t"global pos":[').removesuffix("],\n").split(",")[2])
            rRotation = float(Robot[11].removeprefix('\t\t\t"global rot":[').split(',')[1])
            positionList = [xPositions,YPositions,rRotation]
            return positionList
        except:
            pass

def getMoveList(targetArray,currentArray):
    xDistance = targetArray[0] - currentArray[0]
    yDistance = targetArray[1] - currentArray[1]

    a = targetArray[2] - currentArray[2]
    #print(a)
    b = targetArray[2] - currentArray[2] + 360
    #print(b)
    c = targetArray[2] - currentArray[2] - 360
    #print(c)
    if abs(a) < abs(b) and abs(a) < abs(c):
        rDistance = a
    elif abs(b) < abs(c):
        rDistance = b
    else:
        rDistance = c
    
    moveList = [xDistance,yDistance,rDistance]
    return moveList

def fieldOrient(X,Y,robotHeading):
    hypot = math.hypot(X, Y)
    angle1 = math.degrees(math.atan2(Y, X))
    angle2 = math.radians(robotHeading - angle1-180)
    endX = math.sin(angle2) * hypot
    endY = math.cos(angle2) * hypot
    return [endX, endY,]

def getPIDoutput(moveList):
    RotationMovement = Rpid(moveList[2])
    Xmove = Xpid(moveList[0])
    Ymove = -Ypid(moveList[1])
    return [Xmove,Ymove,RotationMovement]

def writeAuto(moveList):
    inputs["left_x"] = moveList[0]
    inputs["left_y"] = moveList[1]
    inputs["right_x"] = moveList[2]
    AutoMove(inputs)

def AutoMove(inputs):
    with open(PATH + "Controls.txt","w+") as file:
        file.write(Format(inputs))

def Format(inputs):
    return "\n".join(f"{key}={value}" for key,value in inputs.items())

def moveRobot(targetList):
    positionList = getRobotPosition()
    #print(positionList)
    moveList = getMoveList(targetList,positionList)
    #print(moveList)
    moveList = getPIDoutput(moveList)
    #print(moveList)
    moveXY = fieldOrient(moveList[0],moveList[1],positionList[2])
    #print(moveXY)
    toWrite = [moveXY[0],moveXY[1],moveList[2]]
    #print(toWrite)
    writeAuto(toWrite)

