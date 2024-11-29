from cmu_graphics import *
from imageProcessing import getMask
from rooms import Store, Room, Sprite, Shape
#import objectActions

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.playerLevel = 0
    app.backgroundPic = 'assets/shopPlaceholder.jpeg'
    app.store = Store(playerLevel=0, balance=0, currentRoom=lobby)
    lobby = Room('lobby')
    nursery = Room('nursery')
    potting = Room('potting')
    seeding = Room('seeding')
    seedShelf = Room('seedShelf')
    nurseryDoor = Shape(0, 350, 100, 250, fill='pink')
    pottingDoor = Shape(700, 350, 100, 250, fill='pink')
    # lobby.addObject(nurseryDoor, action=lambda: store.switchRoom(nursery), requiredLevel=0)
    # lobby.addObject(pottingDoor, action=lambda: store.switchRoom(potting), requiredLevel=0)

def redrawAll(app):
    print(app.store.currentRoom)
    drawImage(app.backgroundPic, 0, 0, width=app.width, height=app.height)
    if app.store.currentRoom == 'lobby':
        drawRect(0, 350, 100, 250, fill='pink')
        drawLabel('Nursery', 50, 475, size=20)
        drawRect(700, 350, 100, 250, fill='pink')
        drawLabel('Fill orders', 750, 475, size=18)
    elif app.store.currentRoom == 'nursery':
        drawLabel('Nursery Placeholder', 400, 300, size=20)
    elif app.store.currentRoom == 'potting':
        drawLabel('Potting Room Placeholder', 400, 300, size=20)
    elif app.store.currentRoom == 'seeding':
        drawLabel('Seeding Room Placeholder', 400, 300, size=20)
    elif app.store.currentRoom == 'seedShelf':
        drawLabel('Seed Shelf Placeholder', 400, 300, size=20) 
    else:
        app.store.currentRoom = lobby
    for obj in app.store.rooms[currentRoom].roomItems:
        obj.draw()

def onMousePress(app, mouseX, mouseY):
    for obj in app.store.currentRoom.roomItems:
        if obj.x <= mouseX <= obj.x + obj.width and obj.y <= mouseY <= obj.y + obj.height:
            if isIn(mouseX, mouseY, object):
                if app.playerLevel >= requiredLevel:
                    obj.action
                else:
                    print ('f{action} is locked. Reach {requiredLevel} to unlock!')

def isIn(mouseX, mouseY, object):
    if type(object) == Sprite:
        mask = getMask(object)
        if mask[mouseX][mouseY] == 1:
            return True
        else:
            return False
    
def onKeyPress(app, key):
    if key == 'b':
        app.store.currentRoom = 'lobby'

def main():
    runApp()

main()
