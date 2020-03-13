# import Calculations
import time
from gui import carGUI
import random

carListX = []
carListY = []
timeInterval = 1
simluationTime = 1000
carGenerationModulo = 5
maxVelocity = 7.5
DisplayModulo = 5

class Car:

    def __init__(self, length, width, velocityX, velocityY, startX, startY, ID, ETA):
        self.length = length            # Length in meters
        self.width = width              # Width in meters
        self.velocityX = velocityX     # X Velocity in meters/second
        self.velocityY = velocityY     # Y Velocity in meters/second
        self.positionX = startX         # X start coordinate
        self.positionY = startY         # Y start coordinate
        self.ID = ID                    # Give car unique ID
        self.ETA = ETA

    def updatePosition(self, time):
        self.positionX = self.positionX + self.velocityX * time
        self.positionY = self.positionY + self.velocityY * time

    def updateETA(self):
        if (self.velocityX == 0 and self.velocityY == 0):
            self.ETA = self.ETA
        elif(self.velocityX == 0):
            self.ETA = (525 - self.positionY) / self.velocityY
        else:
            self.ETA = (475 - self.positionX) / self.velocityX


def randomCarGenerator(LiveGUI, twoCars, direction):


    ID = randomIDGenerator()
    velocity = maxVelocity * 0.75 + (maxVelocity * 0.25) * float(ID / 10000)

    if(direction == 1):
        # Generate a horizontally traveling car
        car = Car(length=10, width=10, velocityX=velocity, velocityY=0, startX=0, startY=0, ID=ID, ETA = 475)
        LiveGUI.drawCar(direction, ID)

    elif(direction == 2):
        # Generate a vertically traveling car
        car = Car(length=10, width=10, velocityX=0, velocityY=velocity, startX=0, startY=0, ID=ID, ETA = 525)
        LiveGUI.drawCar(direction, ID)

    return car

def timeGenerator():

    timeGene = random.randint(12, 24)
    return timeGene


def randomIDGenerator():
    # Generate a Unique ID
    generateID = True
    while(generateID):
        generateID = False
        ID = random.randint(0, 10000)
        for i in range(0, len(carGUI.carIDs)):
            if ID == carGUI.carIDs[i]:
                generateID = True
    return ID

def simulation(gui):
    random.seed(50)
    elapsedTime = 0                                         # initialize time in seconds
    runSim = True                                           # bool to stop simulation
    count = 0
    lasttime1 = 0
    lasttime2 = 0
    count1 = 0
    count2 = 0
    car1 = -1
    car2 = -1

    while(runSim):

        genTime1 = timeGenerator()
        genTime2 = timeGenerator()
        if((elapsedTime - lasttime1) % genTime1 is 0):
            print(genTime1)
            newCar = randomCarGenerator(gui, True, 1)
            carListX.append(newCar)
            lasttime1 = elapsedTime

        if((elapsedTime - lasttime2) % genTime2 is 0):
            newCar = randomCarGenerator(gui, True, 2)
            carListY.append(newCar)
            lasttime2 = elapsedTime

        if(elapsedTime % DisplayModulo is 0):
            gui.updateCarInformationDisplayX(carListX[count1])
            gui.updateCarInformationDisplayY(carListY[count2])
            gui.updateCarInformationDisplayZ(elapsedTime, count)

        for i in range(len(carListX) -1, -1, -1):
            # THIRD update position
            carListX[i].updatePosition(timeInterval)
            carListX[i].updateETA()
            # etaList.append(carList[i].ETA)
            if carListX[i].ETA <= 0:
                carListX[i].velocityX = min(maxVelocity, carListX[i].velocityX + 0.1)
                if i > 1:
                    carListX[i].velocityX = min(carListX[i].velocityX, carListX[i-1].velocityX)
                # passListX.append(carListX[i])
                if i > car1:
                    count += 1
                    count1 += 1
                    car1 = i
                # del carListX[i]

        for i in range(len(carListY) -1, -1, -1):
            # THIRD update position
            carListY[i].updatePosition(timeInterval)
            carListY[i].updateETA()
            # etaList.append(carList[i].ETA)
            if carListY[i].ETA <= 0:
                carListY[i].velocityY = min(maxVelocity, carListY[i].velocityY + 0.1)
                if i > 1:
                    carListY[i].velocityY = min(carListY[i].velocityY, carListY[i-1].velocityY)
                # passListY.append(carListY[i])
                if i > car2:
                    count += 1
                    count2 += 1
                    car2 = i
                # del carListY[i]

        # slow down X
        while ((carListX[count1].ETA - carListY[count2].ETA >= 0) and (carListX[count1].ETA - carListY[count2].ETA <= 10)):
            carListX[count1].velocityX = max(2, carListX[count1].velocityX - 0.1)
            carListX[count1].updateETA()
            for i in range(1 + count1, len(carListX)):
                carListX[i].velocityX = carListX[i].velocityX \
                                        + 0.1 * (1 - (carListX[i].velocityX / maxVelocity) ** 4 \
                                        - ((20 + max(0, carListX[i].velocityX + carListX[i].velocityX * (carListX[i].velocityX - carListX[i-1].velocityX))) / (carListX[i-1].positionX - carListX[i].positionX - 10)) ** 2)
                if carListX[i].velocityX <= 2:
                    carListX[i].velocityX = 2

        # slow down Y
        while ((carListX[count1].ETA - carListY[count2].ETA <= 0) and (carListX[count1].ETA - carListY[count2].ETA >= -10)):
            carListY[count2].velocityY = max(2, carListY[count2].velocityY - 0.1)
            carListY[count2].updateETA()
            for i in range(1 + count2, len(carListY)):
                carListY[i].velocityY = carListY[i].velocityY \
                                        + 0.1 * (1 - (carListY[i].velocityY / maxVelocity) ** 4 \
                                        - ((20 + max(0, carListY[i].velocityY + carListY[i].velocityY * (carListY[i].velocityY - carListY[i-1].velocityY))) / (carListY[i-1].positionY - carListY[i].positionY - 10)) ** 2)
                if carListY[i].velocityY <= 2:
                    carListY[i].velocityY = 2


        for i in range(1 + count1, len(carListX)):
            carListX[i].velocityX = carListX[i].velocityX \
                                    + 0.1 * (1 - (carListX[i].velocityX / maxVelocity) ** 4 \
                                    - ((20 + max(0, carListX[i].velocityX + carListX[i].velocityX * (carListX[i].velocityX - carListX[i-1].velocityX))) / (carListX[i-1].positionX - carListX[i].positionX - 10)) ** 2)
            if carListX[i].velocityX <= 2:
                carListX[i].velocityX = 2

        for i in range(1 + count2, len(carListY)):
            carListY[i].velocityY = carListY[i].velocityY \
                                    + 0.1 * (1 - (carListY[i].velocityY / maxVelocity) ** 4 \
                                    - ((20 + max(0, carListY[i].velocityY + carListY[i].velocityY * (carListY[i].velocityY - carListY[i-1].velocityY))) / (carListY[i-1].positionY - carListY[i].positionY - 10)) ** 2)
            if carListY[i].velocityY <= 2:
                carListY[i].velocityY = 2



        # Update the GUI positions
        gui.moveCars(carListX, timeInterval)
        gui.moveCars(carListY, timeInterval)

        time.sleep(.05)

        if(elapsedTime > simluationTime):
            runSim = False                                  # if time condition is true runSim to false
        elapsedTime += timeInterval                         # increment 100 mili second
