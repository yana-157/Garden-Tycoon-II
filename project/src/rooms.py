from cmu_graphics import *

class Store:
    def __init__(self, currentRoom, XP=0, playerLevel=0, balance=0):
        self.currentRoom = currentRoom
        self.XP = XP
        self.playerLevel = playerLevel
        self.balance = balance
    def earn(self, payment):
        self.balance += payment
    def earnXP(self, gainedXP):
        self.XP += gainedXP
    def levelUp(self):
        self.playerLevel += 1
    def switchRoom(self, name):
        if name in roomSet:
            self.currentRoom = name

class Room:
    def __init__(self, name):
        self.name = name

class Objects:
    def __init__(self, name, action=None, requiredLevel=0):
        self.name = name
        self.action = action
        self.requiredLevel = requiredLevel

class Shape:
    def __init__(self, x, y, width, height, fill=None, shapeType='rectangle'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.shapeType = shapeType
    def draw(self):
        if self.shapeType == 'rectangle':
            drawRect(
                self.x,
                self.y,
                self.width,
                self.height,
                fill=self.fill
            )
        elif self.shapeType == "circle":
            drawCircle(
                self.x + self.width / 2,
                self.y + self.height / 2,
                self.width / 2,
                fill=self.fill
            )
class Sprite:
    def __init__(self, x, y, width, height, imagePath, action, requiredLevel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.imagePath = imagePath
        self.action = action
        self.requiredLevel = requiredLevel
    def draw(self):
        drawImage(self.imagePath, self.x, self.y, width=self.width, height=self.height)