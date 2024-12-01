from cmu_graphics import *
from imageProcessing import getMask
from rooms import Store, Room, Sprite, Shape
#import objectActions

lobby = Room('lobby')
nursery = Room('nursery')
potting = Room('potting')
seeding = Room('seeding')
seedShelf = Room('seedShelf')
roomSet = {lobby, nursery, potting, seeding, seedShelf}

store = Store(currentRoom = lobby, playerLevel=0, balance=0)

nurseryDoor = Shape(0, 350, 100, 250, fill='pink')
pottingDoor = Shape(700, 350, 100, 250, fill='pink')
lobbyItems = {nurseryDoor, pottingDoor}

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.playerLevel = 0
    app.backgroundPic = 'assets/shopPlaceholder.jpeg'
    store.currentRoom = lobby
    # lobby.addObject(nurseryDoor, action=lambda: store.switchRoom(nursery), requiredLevel=0)
    # lobby.addObject(pottingDoor, action=lambda: store.switchRoom(potting), requiredLevel=0)

def redrawAll(app):
    print(store.currentRoom)
    drawImage(app.backgroundPic, 0, 0, width=app.width, height=app.height)
    if store.currentRoom == lobby:
        nurseryDoor.draw
        drawLabel('Nursery', 50, 475, size=20)
        pottingDoor.draw
        drawLabel('Fill orders', 750, 475, size=18)
    elif store.currentRoom == nursery:
        drawLabel('Nursery Placeholder', 400, 300, size=20)
    elif store.currentRoom == potting:
        drawLabel('Potting Room Placeholder', 400, 300, size=20)
    elif store.currentRoom == seeding:
        drawLabel('Seeding Room Placeholder', 400, 300, size=20)
    elif store.currentRoom == seedShelf:
        drawLabel('Seed Shelf Placeholder', 400, 300, size=20) 
    else:
        store.currentRoom = lobby
#   for obj in app.store.rooms.roomItems:
#       obj.draw()

# def onMousePress(app, mouseX, mouseY):
#     for obj in roomItems:
#         if obj.x <= mouseX <= obj.x + obj.width and obj.y <= mouseY <= obj.y + obj.height:
#             if isIn(mouseX, mouseY, object):
#                 if app.playerLevel >= requiredLevel:
#                     obj.action
#                 else:
#                     print ('f{action} is locked. Reach {requiredLevel} to unlock!')

def isIn(mouseX, mouseY, object):
    if type(object) == Sprite:
        mask = getMask(object)
        if mask[mouseX][mouseY] == 1:
            return True
        else:
            return False
    
def onKeyPress(app, key):
    if key == 'b':
        store.currentRoom = lobby

def main():
    runApp()

main()
