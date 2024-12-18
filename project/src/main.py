from cmu_graphics import *
from imageProcessing import getMask
from classes import Store, Room, Sprite, Shape, Customer, Plant

def switchRoom(app, targetRoom):
        if targetRoom in app.roomSet:
            app.currentRoom = targetRoom
            
def goToNursery(app):
    switchRoom(app, app.nursery)
    
def goToPotting(app):
    switchRoom(app, app.order)

def hasCornerIn(obj, other):
    if ((obj.x <= other.x <= obj.x + obj.width and obj.y <= other.y <= obj.y + obj.height)
        or (obj.x <= other.x + other.width <= obj.x + obj.width and obj.y <= other.y <= obj.y + obj.height)
        or (obj.x <= other.x <= obj.x + obj.width and obj.y <= other.y + other.height <= obj.y + obj.height)
        or (obj.x <= other.x + other.width <= obj.x + obj.width and obj.y <= other.y + other.height <= obj.y + obj.height)
        ):
        return True
    else:
        return False
    
def isInRect(app, mouseX, mouseY, shape):
    app.cx = mouseX
    app.cy = mouseY
    if shape.x <= app.cx <= shape.x + shape.width and shape.y <= app.cy <= shape.y + shape.height:
        return True
    else:
        return False

def overlaps(obj, other): #only rectangles/images being treated as rectangles
    # if isinstance(obj, Shape) and isinstance(other, Shape) :
    return (hasCornerIn(obj, other) or hasCornerIn(other, obj))
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
    
def deletePlant(app, plant):
    app.plantCounts[plant] -= 1

def createNewPlantList(app):
    app.plantList = []
    for plantName in app.plantCounts:
        plantCount = app.plantCounts[plantName]
        while plantCount > 0:
            plant = app.nameObjectDict[plantName]
            plant.width = 50
            plant.height = 75
            app.plantList.append(plant)
            plantCount -= 1

def removeBabyPlant(app, plant):
    app.babyPlantList.remove(plant)

def collectPlant(app, plant):
    if len(app.plantList) >= 18:
        app.popup = 'inventoryFull'
        return
    app.plantCounts[plant.name] = app.plantCounts.get(plant.name, 0) + 1
    createNewPlantList(app)
    removeBabyPlant(app, plant)
    
# def deleteSeedling():
    # clear the slot completely

def generateOrder(app):
    tempList = [app.plantSet]
    difficultyScore = 0
    plant = tempList[0]
#   from a set of plants select a plant
    if app.plantDifficultyDict[plant] == 'easy':
        difficultyScore += 10
    if app.plantDifficultyDict[plant] == 'hard':
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

def isInSprite(app, mouseX, mouseY, item):
    if type(item) == (Sprite or Plant):
        mask = getMask(item, threshold = app.imageThresholdDict[item.name])
        maskX = mouseX - item.x
        maskY = mouseY - item.y
        print(maskX, maskY)
        if mask[maskY][maskX] == 1:
            return True
        else:
            return False

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.playerLevel = 0
    app.backgroundPic = 'assets/lobbySketch.png'
    app.stepsPerSecond = 5
    app.counter = 0
    app.activeOrder = False
    app.lobby = Room('lobby')
    app.nursery = Room('nursery')
    app.seedShelf = Room('seedShelf')
    app.order = Room('order')
    app.roomSet = {app.lobby, app.nursery, app.order, app.seedShelf}
    app.store = Store(currentRoom = app.lobby, XP=0, playerLevel=0, balance=0)
    app.plantCounts = dict()
    app.plantList = []
    app.pinkFlower = Plant('pinkFlower', 300, 300, 100, 200, 'assets/simplePinkFlower.jpeg', 1, 0, canDrag=True)
    app.fiddleLeaf = Plant('fiddleLeaf', 100, 500, 30, 50, 'assets/fiddleLeaf.png', 2, 2, canDrag=True)
    app.plantDifficultyDict = {'pinkFlower': 'easy', 'fiddleLeaf': 'hard'}
    app.placeholderCustomer = Customer('customer', 300, 400, 50, 100, 'assets/customerPlaceholder.png')
    app.nurseryDoor = Shape('nurseryDoor', 0, 250, 100, 250, 'pink', 'rectangle', goToNursery)
    app.orderDoor = Shape('orderDoor', 700, 250, 100, 250, 'pink', 'rectangle', goToPotting)
    app.garbageCan = Shape('garbageCan', 525, 350, 75, 100, 'gray', 'rectangle', deletePlant)
    app.lobbyItemList = [app.nurseryDoor, app.orderDoor, app.garbageCan]
    app.lobbyItemDict = {'nurseryDoor': (0, goToNursery), 'orderDoor': (0, goToPotting), 'garbageCan': (0, deletePlant)}
    app.nurseryItemActionsDict = {'pinkFlower': (0, collectPlant)}
    app.nameObjectDict = {'pinkFlower': app.pinkFlower,
                          'fiddleLeaf': app.fiddleLeaf,
                          'nurseryDoor': app.nurseryDoor,
                          'orderDoor': app.orderDoor,
                          'garbageCan': app.garbageCan
                          }
    app.nonPlantNurseryItems = []
    app.babyPlantList = [app.pinkFlower]
    app.currentRoom = app.lobby
    app.popup = 'inventoryFull'
    app.imageThresholdDict = {'pinkFlower': 215}
    app.distFromTop = None
    app.distFromLeft = None
    app.draggedObj = None
    app.dismissPopup = Shape('Dismiss', 200, 200, 20, 20, 'red', 'rectangle', dismissPopup)

def dismissPopup(app):
    app.popup = None

def redrawAll(app):
    print(app.currentRoom)
    if app.currentRoom == app.lobby:
        drawImage(app.backgroundPic, 0, 0, width=app.width, height=app.height)
        for item in app.lobbyItemList:
            item.draw()
        drawLabel('Nursery', 50, 375, size=20)
        drawLabel('Fill orders', 750, 375, size=20)
        #logic for drawing plants in inventory in the correct slots on shelves!!
        for i in range(len(app.plantList)):
            plant = app.plantList[i]
            plant.height = 75
            plant.width = 50
            if (i+1)%6 < 4:
                plant.x = 125 + 75*i
                if i == 0 or i//6 == 1:
                    plant.y = 62.5
                if i//6 == 2:
                    plant.y = 150
                if i//6 == 3:
                    plant.y = 287.5
            else:
                plant.x = 475 + 75*(i-3)
                if i//6 == 1:
                    plant.y = 62.5
                if i//6 == 2:
                    plant.y = 150
                if i//6 == 3:
                    plant.y = 287.5
            plant.properShelfPosition = (plant.x,plant.y)
            plant.draw()
        # make sure to draw last, after customer and everything:
        drawImage('assets/woodGrain.webp', 0, 450, width=app.width, height=150)
    elif app.currentRoom == app.nursery:
        # app.background == {'nursery image'}
        drawLabel('Nursery Placeholder', 400, 300, size=20)
        for item in app.nonPlantNurseryItems:
            item.draw()
        for plant in app.babyPlantList:
            plant.draw()
    elif app.currentRoom == app.order:
        drawLabel('Order Room Placeholder', 400, 300, size=20)
    elif app.currentRoom == app.seedShelf:
        drawLabel('Seed Shelf Placeholder', 400, 300, size=20)
    if app.popup == 'inventoryFull':
        drawRect(200, 200, 400, 200, fill='white', border='black')
        drawLabel('Inventory is full! Sell or delete a plant', 400, 300, size=20)
        drawLabel('to make room for new plants!', 400, 325, size=20)
        app.dismissPopup.draw()
    if app.popup == 'levelAlert':
        drawRect(200, 200, 400, 200, fill='white', border='black')
        drawLabel('This feature is locked. Reach a higher level to unlock!', 400, 300, size=20)

def onMousePress(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY
    if app.popup:
            if isInRect(app, mouseX, mouseY, app.dismissPopup):
                app.dismissPopup.action(app)
    if app.currentRoom == app.lobby:
        for obj in app.lobbyItemList:
            reqLevel, action = app.lobbyItemDict[obj.name]
            if type(obj) == Sprite:
                if isInSprite(app, mouseX, mouseY, obj):
                    if app.playerLevel >= reqLevel:
                        action()
                    else:
                        app.popup = 'levelAlert'
            elif type(obj) == Shape:
                if isInRect(app, mouseX, mouseY, obj):
                    if app.playerLevel >= reqLevel:
                        action(app)
                    else:
                        app.popup = 'levelAlert'
        for plant in app.plantList:
            if isInRect(app, mouseX, mouseY, plant):
                app.draggedObj = plant
                app.distFromTop = app.cy - plant.y
                app.distFromLeft = app.cx - plant.x       
    if app.currentRoom == app.nursery:
        for obj in app.nonPlantNurseryItems:
            reqLevel, action = app.nurseryItemActionsDict[obj.name]
            # does not work at the moment so i will debug the getMask stuff and get back to this
            # if type(obj) == Sprite:
            #     if isInSprite(app, mouseX, mouseY, obj):
            #         if app.playerLevel >= reqLevel:
            #             action(app)
            #         else:
            #             app.popup = 'levelAlert'
            if type(obj) == Shape:
                if isInRect(app, mouseX, mouseY, obj):
                    if app.playerLevel >= reqLevel:
                        action(app)
                    else:
                        app.popup = 'levelAlert'
        tempList = app.babyPlantList[:]
        print(tempList)
        for babyPlant in tempList:
            #something to check if its within bounds, then select the correct plant object
            # print(isInSprite(app, mouseX, mouseY, babyPlant))
            # if isInSprite(app, mouseX, mouseY, babyPlant):
            if isInRect(app, mouseX, mouseY, babyPlant):
                collectPlant(app, babyPlant)
                print(mouseX, mouseY)
                print(f'collected {babyPlant.name}')

def onMouseDrag(app, mouseX, mouseY):
    if app.draggedObj and app.draggedObj.canDrag:
        app.draggedObj.x = (mouseX - app.distFromLeft)
        # had written + rather than -, chatGPT found this bug (rest of what it said was useless, I still have not been able to fix it
        # just used the part where it said to change the sign)
        #: https://chatgpt.com/share/674e0ef3-3804-8001-ac34-237d87ed557f
        app.draggedObj.y = (mouseY - app.distFromTop)
                      
def onMouseRelease(app, mouseX, mouseY):
    if app.currentRoom == app.lobby:
        if type(app.draggedObj) == Plant:
            if overlaps(app.draggedObj, app.garbageCan):
                deletePlant(app, app.draggedObj)
            else:
                app.draggedObj.x, app.draggedObj.y = app.draggedObj.properShelfPosition
    app.draggedObj = None

def onKeyPress(app, key):
    if key == 'b':
        app.currentRoom = app.lobby

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
#   draw customer off to the side waiting

# draw order:
#   draw the background of the order form
#   place customer name at the top
#   list the required plant, soil types, pot color, and decorations
#   draws the order, starting with the plant, then pot, then decorations
#   soil order is drawn in a rectangle on the side

# random number selector(number):
#   generate a number from 0-number

# def customerEmotions
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
