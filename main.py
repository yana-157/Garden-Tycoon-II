from cmu_graphics import *
from imageProcessing import getMask
from rooms import Store, Room, Sprite, Shape
#import objectActions

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.playerLevel = 0
    app.backgroundPic = 'assets/shopPlaceholder.jpeg'
    app.store = Store()
    lobby = Room('lobby')
    nursery = Room('nursery')
    potting = Room('potting')
    seeding = Room('seeding')
    seedShelf = Room('seedShelf')
    nurseryDoor = Shape(0, 350, 100, 250, fill='pink')
    pottingDoor = Shape(700, 350, 100, 250, fill='pink')
    lobby.addObject(nurseryDoor, action=lambda: app.store.switchRoom('nursery'), requiredLevel=0)
    lobby.addObject(pottingDoor, action=lambda: app.store.switchRoom('potting'), requiredLevel=0)
    app.store.switchRoom('lobby')
    app.store.addRoom(lobby)
    app.store.addRoom(nursery)
    app.store.addRoom(potting)
    app.store.addRoom(seeding)
    app.store.addRoom(seedShelf)
    app.store.currentRoom = 'lobby'

def draw(app):
    if app.store.currentRoom == 'lobby':
        drawRect(0, 350, 100, 250, fill='pink')
        drawLabel('Nursery', 50, 475, size=20, action=app.store.switchRoom('nursery'), requiredLevel=0)
        drawRect(700, 350, 100, 250, fill='pink', action=app.store.switchRoom('potting'), requiredLevel=0)
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

def redrawAll(app):
    drawImage(app.backgroundPic, 0, 0, width=app.width, height=app.height)
    currentRoom = app.store.currentRoom
    for obj in currentRoom.objects:
        draw(obj)

def onMousePress(app, mouseX, mouseY):
    currentRoom = app.store.currentRoom
    for obj in currentRoom.objects:
        if obj.x <= mouseX <= obj.x + obj.width and obj.y <= mouseY <= obj.y + obj.height:
            if isIn(mouseX, mouseY, object):
                action, requiredLevel = objectActions[obj]
                if playerLevel >= requiredLevel:
                    action
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
