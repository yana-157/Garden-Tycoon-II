from cmu_graphics import *
from imageProcessing import getMask
from classes import Store, Room, Sprite, Shape, Customer, Plant

lobby = Room('lobby')
nursery = Room('nursery')
seedShelf = Room('seedShelf')
order = Room('order')
roomSet = {lobby, nursery, order, seedShelf}

store = Store(currentRoom = lobby, XP=0, playerLevel=0, balance=0)

plantCounts = dict()
plantList = []

pinkFlower = Plant('pinkFlower', 100, 500, 30, 50, 'assets/simplePinkFlower.jpeg', 1, 0, canDrag=True)
fiddleLeaf = Plant('pinkFlower', 100, 500, 30, 50, 'assets/fiddleLeaf.png', 2, 2, canDrag=True)

plantDifficultyDict = {pinkFlower: 'easy', fiddleLeaf: 'hard'}

placeholderCustomer = Customer('customer', 300, 400, 50, 100, 'assets/customerPlaceholder.png')

def switchRoom(targetRoom):
        if targetRoom in roomSet:
            store.currentRoom = targetRoom
            
def goToNursery():
    switchRoom(nursery)
    
def goToPotting():
    switchRoom(order)

def hasCornerIn(obj, other):
    if (obj.x <= other.x <= obj.x + obj.width and obj.y <= other.y <= obj.y + obj.height
        or obj.x <= other.x + other.width <= obj.x + obj.width and obj.y <= other.y <= obj.y + obj.height
        or obj.x <= other.x <= obj.x + obj.width and obj.y <= other.y + other.height <= obj.y + obj.height
        or obj.x <= other.x + other.width <= obj.x + obj.width and obj.y <= other.y + other.height <= obj.y + obj.height
        ):
        return True
    else:
        return False
    
def isInRect(mouseX, mouseY, shape):
    if shape.x <= mouseX <= shape.x + shape.width and shape.y <= mouseY <= shape.y + shape.height:
        return True
    else:
        return False

def overlaps(obj, other): #only rectangles/images being treated as rectangles
    # if isinstance(obj, Shape) and isinstance(other, Shape) :
    if hasCornerIn(obj, other):
        return True
    else:
        return False
    # if isinstance(obj, Sprite) and isinstance(other, Shape):
    #     if hasCornerIn(obj, other):
    #         objPath, threshold = spriteDict[obj]
    #         for row in getMask(objPath, threshold):
    #             for pixel in row:
    #                 if pixel == 1 and # is in 
    #     else:
    #         return False
    # if isinstance(obj, Shape) and isinstance(other, Sprite):
    #    if hasCornerIn(obj, other)
    # if isinstance(obj, Sprite) and isinstance(other, Sprite):
    
def deletePlant(plant):
    plantCounts[plant] -= 1

nurseryDoor = Shape('nurseryDoor', 0, 350, 100, 250, 'pink', 'rectangle', goToNursery)
orderDoor = Shape('orderDoor', 700, 350, 100, 250, 'pink', 'rectangle', goToPotting)
garbageCan = Shape('garbageCan', 350, 350, 100, 100, 'gray', 'rectangle', deletePlant)
lobbyItemDict = {nurseryDoor: (0, nurseryDoor.action), orderDoor: (0, orderDoor.action), garbageCan: (0, garbageCan.action)}

def createNewPlantList():
    for plant in plantCounts:
        plantCount = plantCounts[plant]
        while plantCount > 1:
            plantList = []
            plantCount = plantCounts[plant]
            plantList.append(plant)

def collectPlant(plant):
    if len(plantList) > 18:
        store.popup = 'inventoryFull'
        return
    plantCounts[plant] = plantCounts.get(plant, 0) + 1
    createNewPlantList()
            
nurseryItemDict = {pinkFlower: (collectPlant(pinkFlower), 0)}
babyPlantCounts = {pinkFlower: 1}
    
# def deleteSeedling():
    # clear the slot completely

def generateOrder():
    tempList = [plantSet]
    difficultyScore = 0
    plant = tempList[0]
#   from a set of plants select a plant
    if plantDifficultyDict[plant] == 'easy':
        difficultyScore += 10
    if plantDifficultyDict[plant] == 'hard':
        difficultyScore += 20
#   generate a number between 1 and 4
#       select that number of soils
#   difficulty score += number/3
#   select the required order of soils by setting that set to a list, which will automatically create a random order
#   generate a number between 1 and 4
#       select the pot type corresponding to the number
#   generate a number between 1 and 4
#       select the decoration corresponding to the number
#   create order class instance containing all this info

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.playerLevel = 0
    app.backgroundPic = 'assets/shopPlaceholder.jpeg'
    app.stepsPerSecond = 5
    app.counter = 0
    app.activeOrder = False
    store.currentRoom = lobby

def redrawAll(app):
    print(store.currentRoom)
    if store.popup == 'inventoryFull':
        drawRect(200, 200, 400, 200, fill='white', border='black')
        drawLabel('Inventory is full! Sell or delete a plant to make room for new plants!', 400, 300, size=20)
    if store.currentRoom == lobby:
        drawImage(app.backgroundPic, 0, 0, width=app.width, height=app.height)
        for item in lobbyItemDict:
            item.draw()
        drawLabel('Nursery', 50, 475, size=20)
        drawLabel('Fill orders', 750, 475, size=20)
    elif store.currentRoom == nursery:
        # app.background == {'nursery image'}
        drawLabel('Nursery Placeholder', 400, 300, size=20)
        for item in nurseryItemDict:
            item.draw()
    elif store.currentRoom == order:
        drawLabel('Order Room Placeholder', 400, 300, size=20)
    elif store.currentRoom == seedShelf:
        drawLabel('Seed Shelf Placeholder', 400, 300, size=20)

def onMousePress(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY
    if store.currentRoom == lobby:
        for obj in lobbyItemDict:
            reqLevel, action = lobbyItemDict[obj]
            if type(obj) == Sprite:
                if isInSprite(mouseX, mouseY, obj):
                    if app.playerLevel >= reqLevel:
                        action()
                    else:
                        print (f'This feature is locked. Reach {obj.requiredLevel} to unlock!')
            elif type(obj) == Shape:
                if isInRect(mouseX, mouseY, obj):
                    if app.playerLevel >= reqLevel:
                        action()
                    else:
                        print ('f{action} is locked. Reach {requiredLevel} to unlock!')
    if store.currentRoom == nursery:
        for obj in nurseryItemDict:
            reqLevel, action = nurseryItemDict[obj]
            if type(obj) == Sprite:
                SpriteImage = obj.imagePath
                if isInSprite(mouseX, mouseY, SpriteImage):
                    if app.playerLevel >= reqLevel:
                        action()
                    else:
                        print (f'This feature is locked. Reach {obj.requiredLevel} to unlock!')
            elif type(obj) == Shape:
                if isInRect(mouseX, mouseY, obj):
                    if app.playerLevel >= reqLevel:
                        action()
                    else:
                        print (f'This feature is locked. Reach {obj.requiredLevel} to unlock!')

def onMouseDrag(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY
    if store.currentRoom == lobby:
        for obj in lobbyItemDict:
            if type(obj) == Sprite:
                if isInSprite(app.cx, app.cy, obj):
                    if obj.canDrag == True:
                        obj.x += app.cx
                        obj.y += app.cy
            if type(obj) == Shape:
                if isInRect(app.cx, app.cy, obj):
                    if obj.canDrag == True:
                        obj.x += app.cx
                        obj.y += app.cy
    if store.currentRoom == nursery:
        for obj in nurseryItemDict:
            if type(obj) == Sprite:
                SpriteImage = obj.imagePath
                if isInSprite(app.cx, app.cy, SpriteImage):
                    if obj.canDrag == True:
                        obj.x += app.cx
                        obj.y += app.cy
            if type(obj) == Shape:
                if isInRect(app.cx, app.cy, obj):
                    if obj.canDrag == True:
                        obj.x += app.cx
                        obj.y += app.cy
                      
def onMouseRelease(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY
    if store.currentRoom == lobby:
        for plant in plantCounts:
            if overlaps(plant, garbageCan):
                deletePlant(plant)

def isInSprite(mouseX, mouseY, item):
    if type(item) == Sprite:
        mask = getMask(item)
        if mask[mouseX - item.x][mouseY - item.y] == 1:
            return True
        else:
            return False
    
def onKeyPress(app, key):
    if key == 'b':
        store.currentRoom = lobby
        
def onStep(app):
    app.counter += 1

def main():
    runApp()

main()

# customer approach:
#   !generate customer appearance!
#   !generate customer name!, which will display over the customer's head
#   customer walks to the counter in a set amount of time, growing larger and moving slightly downwards as they approach

def onCustomerArrival():
    placeholderCustomer.order = generateOrder()
    app.activeOrder = True
#   when you click collect order: !store the order in orders list!
#   start timer to determine rating of order filling

# draw order:
#   draw the background of the order form
#   place customer name at the top
#   list the required plant, soil types, pot color, and decorations
#   draws the order, starting with the plant, then pot, then decorations
#   soil order is drawn in a rectangle on the side

# random number selector(number):
#   generate a number from 0-number

# def customerEmotions(Customer, )
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
#   after plant is fully green the icon will change to say click to add seedlings to inventory
#   seedlings in inventory will show up in the lobby on shelves beside the door
#   garbage can in lobby-> can drag seedlings to garbage if needed, there is limited inventory space
#   if inventory is full, popup tells you can fill orders or delete plants


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
