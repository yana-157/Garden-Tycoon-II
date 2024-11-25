class Store:
	def __init__(self):
		self.rooms = dict()
		self.currentRoom = None
	def addRoom(self, room):
		self.rooms[room.name] = room
	def switchRoom(self, roomName):
		if roomName in self.rooms:
			self.currentRoom = roomName

class Room:
	def __init__(self, name):
		self.name = name
		self.objectActions = dict{}
	def addObject(self, obj, action=None, requiredLevel=0):
		self.objectActions[obj] = (action, requiredLevel)

class Shape:
    def __init__(self, x, y, width, height, fill=None, shapeType='rectangle', action=None, requiredLevel=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.shapeType = shapeType
        self.action = action
        self.requiredLevel = requiredLevel
    def draw(self):
        if self.shapeType == "rectangle":
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
	def __init__(self, x, y, width, height, imagePath, action=None, requiredLevel=0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.imagePath = imagePath
		self.action = action
		self.requiredLevel = requiredLevel
		self.image = None
	def draw(self):
		drawImage(self.imagePath, self.x, self.y, width=self.width, height=self.height)
