from cmu_graphics import *
from imageProcessing import getMask

class Store:
    def __init__(self, currentRoom, XP=0, playerLevel=0, balance=0, popup = None):
        self.currentRoom = currentRoom
        self.XP = XP
        self.playerLevel = playerLevel
        self.balance = balance
        self.popup = popup
    def earn(self, payment):
        self.balance += payment
    def earnXP(self, gainedXP):
        self.XP += gainedXP
    def levelUp(self):
        self.playerLevel += 1

class Room:
    def __init__(self, name):
        self.name = name

class Item:
    def __init__(self, name, x, y, width, height, action=None, requiredLevel=0, canDrag=False):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.requiredLevel = requiredLevel
        self.canDrag = canDrag

class Shape(Item):
    def __init__(self, name, x, y, width, height, fill=None, shapeType='rectangle', action=None, requiredLevel=0, canDrag=False):
        super().__init__(name, x, y, width, height, action, requiredLevel, canDrag)
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
        elif self.shapeType == 'circle':
            drawCircle(
                self.x + self.width / 2,
                self.y + self.height / 2,
                self.width / 2,
                fill=self.fill
            )
class Sprite(Item):
    def __init__(self, name, x, y, width, height, imagePath, action=None, requiredLevel=0, canDrag=False):
        super().__init__(name, x, y, width, height, action, requiredLevel, canDrag=False)
        self.imagePath = imagePath
    def draw(self):
        drawImage(self.imagePath, self.x, self.y, width=self.width, height=self.height)
        
class Plant(Sprite):
    def __init__(self, name, x, y, width, height, imagePath, growTime, properShelfPosition=(0,0), price=0, action=None, requiredLevel=0, canDrag=False):
        super().__init__(name, x, y, width, height, imagePath, action=None, requiredLevel=0, canDrag=False)
        self.growTime = growTime
        self.price = price
        properShelfPosition = properShelfPosition

class Order(Item):
    def __init__(self, name, x, y, width, height, potColor, plant, soils, decoration, difficulty):
        super().__init__(name, x, y, width, height)
        self.plant = plant
        self.potColor = potColor
        self.soils = soils
        self.decoration = decoration
        self.difficulty = difficulty

class Customer(Sprite):
    def __init__(self, name, x, y, width, height, imagePath, allottedTime=10, canDrag=False, order=None, emotion='happy'):
        super().__init__(name, x, y, width, height, imagePath, canDrag=False)
        self.order = order
        self.allottedTime = allottedTime
        self.emotion = emotion
    