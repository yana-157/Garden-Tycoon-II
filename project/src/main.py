from cmu_graphics import *
from imageProcessing import getMask
from rooms import Store, Room, Sprite, Shape

lobby = Room('lobby')
nursery = Room('nursery')
seedShelf = Room('seedShelf')
order = Room('order')
roomSet = {lobby, nursery, order, seedShelf}

store = Store(currentRoom = lobby, XP=0, playerLevel=0, balance=0)

def switchRoom(targetRoom):
        if targetRoom in roomSet:
            store.currentRoom = targetRoom
            
def goToNursery():
    switchRoom(nursery)
    
def goToPotting():
    switchRoom(order)

nurseryDoor = Shape(0, 350, 100, 250, fill='pink', shapeType='rectangle')
orderDoor = Shape(700, 350, 100, 250, fill='pink', shapeType='rectangle')
lobbyItemDict = {nurseryDoor: (0, goToNursery), orderDoor: (0, goToPotting)}

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.playerLevel = 0
    app.backgroundPic = 'assets/shopPlaceholder.jpeg'
    store.currentRoom = lobby

def redrawAll(app):
    print(store.currentRoom)
    if store.currentRoom == lobby:
        drawImage(app.backgroundPic, 0, 0, width=app.width, height=app.height)
        nurseryDoor.draw()
        print()
        drawLabel('Nursery', 50, 475, size=20)
        orderDoor.draw()
        drawLabel('Fill orders', 750, 475, size=18)
    elif store.currentRoom == nursery:
        # app.background == {'color'}
        drawLabel('Nursery Placeholder', 400, 300, size=20)
    elif store.currentRoom == order:
        drawLabel('Order Room Placeholder', 400, 300, size=20)
    elif store.currentRoom == seedShelf:
        drawLabel('Seed Shelf Placeholder', 400, 300, size=20)

def onMousePress(app, mouseX, mouseY):
    if store.currentRoom == lobby:
        for obj in lobbyItemDict:
            reqLevel, action = lobbyItemDict[obj]
            if type(obj) == Sprite:
                if isInSprite(mouseX, mouseY, obj):
                    if app.playerLevel >= reqLevel:
                        action()
                    else:
                        print ('f{action} is locked. Reach {requiredLevel} to unlock!')
            elif type(obj) == Shape:
                if obj.x <= mouseX <= obj.x + obj.width and obj.y <= mouseY <= obj.y + obj.height:
                    if app.playerLevel >= reqLevel:
                        action()
                    else:
                        print ('f{action} is locked. Reach {requiredLevel} to unlock!')

def isInSprite(mouseX, mouseY, object):
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

# customer approach:
#   generate customer appearance
#   generate customer name, which will display over the customer's head
#   customer walks to the counter in a set amount of time, growing larger as it approaches

# generate customer:
#   generate a number between 1 and 2
#   select customer gender: 1 male, 2 female
#   create a mask of a {gender} customer that I've colored in primary colors
#   generate a number between 1 and 3
#   select a skin color from the list and color in the skin this color
#   generate another number
#   select a hair color by indexing into a list, set hair to this color-- remove if bald
#   generate another number
#   select a shirt color by indexing into a list, set shirt to this color
#   generate another number
#   select a pants color by indexing into a list, set pants to this color

# on customer arrival:
#   when the customer arrives, !generate order!
#   !assign difficulty score! to order based on plant rarity and number of components
#   !draw the order form!
#   !store the order in orders list!, with the most recent order appearing first
#   start timer to determine rating of order filling

# generate order:
#   difficulty score is a property of the order
#   from a set of plants select a plant
#   difficulty score += plantDifficultyDict[plant]
#   generate a number between 1 and 4
#       select that number of soils
#   difficulty score += number/3
#   select the required order of soils by setting that set to a list, which will automatically create a random order
#   generate a number between 1 and 4
#       select the pot type corresponding to the number
#   generate a number between 1 and 4
#       select the decoration corresponding to the number
#   create order class instance containing all this info

# draw order:
#   draw the background of the order form
#   place customer name at the top
#   list the required plant, soil types, pot color, and decorations
#   draws the order, starting with the plant, then pot, then decorations
#   soil order is drawn in a rectangle on the side

# random number selector(number):
#   generate a number from 0-number

# customer emotions:
#   starts out happy
#   as the timer runs out for the order, the customer grows more upset
#   if half of the time has elapsed:
#       customer becomes neutral
#       expression is set to neutral
#   if 3/4 of the time has elapsed:
#       customer becomes annoyed
#       expression is set to annoyed
#   if time runs out:
#       customer becomes angry
#       expression is set to angry

# nursery:
#   each slot will have a message that says drag seedling tray to begin planting
#   currently selected seeds will display in a window next to the shelf
#   drag seeding tray to slot, implement snapping if any part overlaps
#   draw tray in that slot
#   message there will then change to add soil
#   drag soil to tray, on mouse release tay will fill with soil
#   message will then become click to plant, or select seed packet from shelf to change plant
#   when u click the shelf the !seed shelf opens!
#   after clicking to plant seeds will be drawn on the tray
#   once seeds are added message changes to drag watering can to water
#   on mouse release soil will become darker
#   immediately an icon will appear as a white circle with a black border, above the tray
#   as the plant grows the icon will fill in like a dial
#   growth and icon filling will occur at a speed that is proportional to the grow time of the plant


# order fulfilment room:
#   draw order filling box
#   must select pot before anything else-- if u try to click on anything else, message that says select pot first will appear
#   selecting a soil adds it to the pot, with the pot transparent at this stage.
#   plant the plant by clicking "plant" button, which plants the most recently selected plant
#   select decoration, pot turns opaque
#   click 'finish order" to fade back into the lobby, order ticket will be marked as resolved now


# order scoring and pricing:
#   amt of money earned assigned based on score
#   difficulty sets the ceiling
#   if soil order is messed up but soils are correct: 10% deduction
#   if soils are not correct: 20% deduction
#   if pot color is wrong: 20% deduction
#   if decoration is wrong: 10% deduction
#   if plant type is wrong: 50% deduction
#   happy customer gives a tip equal to 25% (125% earned), neutral no tip, annoyed demands discount (50% earned), angry no payment
