from functions import *

class Object:
	def __init__(self, position, rotation, scale, objSpaceVertexTable, triTable):
		self.pos = position
		self.rot = rotation				#always in radians
		self.rotDeg = rotation
		self.scl = scale

		self.objSpaceVertexTable = objSpaceVertexTable.copy()
		self.wldSpaceVertexTable = full((len(objSpaceVertexTable), 3), 0, dtype=float)
		self.triTable = triTable.copy()
		self.updateWldSpaceVertexTable()

	def updateWldSpaceVertexTable(self):

		translationMatrix = array([				# translation matrix
			[1, 0, 0, self.pos[0]],
			[0, 1, 0, self.pos[1]],
			[0, 0, 1, self.pos[2]],
			[0, 0, 0, 1]])
		
		xRotMatrix = array([					# x-axis rotation matrix
			[1, 0, 0, 0],
			[0, cos(self.rot[0]), sin(self.rot[0]), 0],
			[0, -sin(self.rot[0]), cos(self.rot[0]), 0],
			[0, 0, 0, 1]
		])
		yRotMatrix = array([					# y-axis rotation matrix
			[cos(self.rot[1]), 0, -sin(self.rot[1]), 0],
			[0, 1, 0, 0],
			[sin(self.rot[1]), 0, cos(self.rot[1]), 0],
			[0, 0, 0, 1]
		])
		zRotMatrix = array([					# z-axis rotation matrix
			[cos(self.rot[2]), sin(self.rot[2]), 0, 0], 
			[-sin(self.rot[2]), cos(self.rot[2]), 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]
		])

		rotationMatrix = xRotMatrix @ yRotMatrix @zRotMatrix #compound rotation matrix

		scaleMatrix = array([
		[self.scl[0], 0, 0, 0],
		[0, self.scl[1], 0, 0],
		[0, 0, self.scl[2], 0],
		[0, 0, 0, 1]])

		transformationMatrix = translationMatrix @ rotationMatrix @ scaleMatrix

		for vertex in range(len(self.objSpaceVertexTable)):
			self.wldSpaceVertexTable[vertex] = delete((transformationMatrix @ append(self.objSpaceVertexTable[vertex],1).T).T,3)
			
	def translate(self, posDifference):
		self.pos = self.pos + posDifference # update position variable
		self.updateWldSpaceVertexTable()
	
	def rotate(self, rotDifference):
		self.rot = self.rot + rotDifference
		for val in range(len(self.rotDeg)):
			self.rotDeg[val] = d(self.rot[val])
		self.updateWldSpaceVertexTable()

	def scale(self, sclDifference):
		self.scl = self.scl * sclDifference
		self.updateWldSpaceVertexTable()
	
	def setPosition(self, newPos):
		self.pos = newPos
		self.updateWldSpaceVertexTable()

	def setRotation(self, newRot):
		self.rot = newRot.copy()
		for val in range(len(self.rotDeg)):
			self.rotDeg[val] = d(self.rot[val])
		self.updateWldSpaceVertexTable()
	
	def setScale(self, newScl):
		self.scl = newScl
		self.updateWldSpaceVertexTable()
	
	def setGeometry(self, newObjVertexTable, newEdgeTable, newSurfaceTable):
		self.objSpaceVertexTable = newObjVertexTable
		self.wldSpaceVertexTable = newObjVertexTable
		self.updateWldSpaceVertexTable()
		self.edgeTable = newEdgeTable
		self.surfaceTable = newSurfaceTable

class Empty:
	def __init__(self, position = array([0,0,0]), rotation = array([0,0,0]), scale = array([1,1,1])):
		self.pos = position
		self.rot = rotation				#always in radians
		self.rotDeg = rotation
		self.scl = scale
	
	def translate(self, posDifference):
		self.pos = self.pos + posDifference # update position variable
	
	def rotate(self, rotDifference):
		self.rot = self.rot + rotDifference
		for val in range(len(self.rotDeg)):
			self.rotDeg[val] = d(self.rot[val])

	def scale(self, sclDifference):
		self.scl = self.scl * sclDifference
	
	def setPosition(self, newPos):
		self.pos = newPos

	def setRotation(self, newRot):
		self.rot = newRot
		for val in range(len(self.rotDeg)):
			self.rotDeg[val] = d(self.rot[val])
	
	def setScale(self, newScl):
		self.scl = newScl

class Camera:
	def __init__(self, position = array([0,0,0]), rotation = array([0,0,0]), scale = array([1,1,1]), fieldOfView = r(30), shiftX = 0, shiftY = 0, nearZ = 0.1, farZ = 5):
		self.pos = position
		self.rot = rotation				#always in radians
		self.rotDeg = rotation			#rotation in degrees - do not write to except to change it to reflect self.rot
		self.scl = scale
		self.FOV = fieldOfView
		self.sX = shiftX
		self.sY = shiftY
		self.nearZ = nearZ
		self.farZ = farZ

		for val in range(len(self.rotDeg)):
			self.rotDeg[val] = d(self.rot[val])
	
	def translate(self, posDifference):
		self.pos = self.pos + posDifference
	
	def rotate(self, rotDifference):
		self.rot = self.rot + rotDifference
		for val in range(len(self.rotDeg)):
			self.rotDeg[val] = d(self.rot[val])

	def scale(self, sclDifference):
		self.scl = self.scl * sclDifference

	def changeFL(self, fLDifference):
		self.fL = self.fL + fLDifference
	
	def shiftViewPlane(self, diffX, diffY):
		self.sX = self.sX + diffX
		self.sY = self.sY + diffY
	
	def setPosition(self, newPos):
		self.pos = newPos

	def setRotation(self, newRot):
		self.rot = newRot
		for val in range(len(self.rotDeg)):
			self.rotDeg[val] = d(self.rot[val])
	
	def setScale(self, newScl):
		self.scl = newScl
	
	def setFOV(self, newFOV):
		self.FOV = newFOV

	def setZClipping(self, newNearZ, newFarZ):
		self.nearZ = newNearZ
		self.farZ = newFarZ

class Screen:
	def __init__(self, width, height):
		self.pixels = full((width, height, 3), 0, dtype=uint8)
		self.res = (width, height)
		self.height = height
		self.width = width
		self.aspectRatio = width/height
	
	def drawPixel(self, point, color):
		pixelX, pixelY = point
		# print(str(pX) + ' ' + str(pY))
		if (pixelX >= self.width or (self.height-pixelY) >= self.height) or (pixelX < 0 or (self.height-pixelY) < 0): #if i try to draw off the screen array, just /dont/
				return
		self.pixels[pixelX][self.height-pixelY] = color #fixes screen orientation bug, sets 0,0 to bottom left corner instead of top left
	
	def drawLine(self, point0, point1, color): #bresenham magic
		x0, y0 = point0[0], point0[1]
		x1, y1 = point1[0], point1[1]
		dx = abs(x1 - x0)
		sx = 1 if x0 < x1 else -1
		dy = -abs(y1 - y0)
		sy = 1 if y0 < y1 else -1
		error = dx + dy
	
		while True:
			self.drawPixel((x0, y0), color)
			if (x0 == x1) and (y0 == y1):
				break
			e2 = 2 * error
			if e2 >= dy:
				if x0 == x1:
					break
				error = error + dy
				x0 = x0 + sx
			if e2 <= dx:
				if y0 == y1:
					break
				error = error + dx
				y0 = y0 + sy
	
	def drawTriangle(self, point0, point1, point2, color): #bresenham magic
		x0, y0 = point0[0], point0[1]
		x1, y1 = point1[0], point1[1]
		dx = abs(x1 - x0)
		sx = 1 if x0 < x1 else -1
		dy = -abs(y1 - y0)
		sy = 1 if y0 < y1 else -1
		error = dx + dy
	
		while True:
			# if (x0 >= self.width or y0 >= self.height) or (x0 < 0 or y0 < 0): #if i try to draw off the screen array, just /dont/
			# 	return
			self.drawLine((x0, y0), point2, color)
			if (x0 == x1) and (y0 == y1):
				break
			e2 = 2 * error
			if e2 >= dy:
				if x0 == x1:
					break
				error = error + dy
				x0 = x0 + sx
			if e2 <= dx:
				if y0 == y1:
					break
				error = error + dx
				y0 = y0 + sy
		
	def fill(self, color):
		self.pixels = full((self.width, self.height, 3), color)
	
	def clear(self):
		self.pixels = full((self.width, self.height, 3), 0, dtype=uint8)

class Scene:
	def __init__(self, backgroundColor = array([0,0,0]), backfaceCulling = True):
		self.objectCollection = empty(0, dtype=Object)
		self.bg = backgroundColor
		self.backfaceCulling = backfaceCulling

	def addObjectToScene(self, obj):
		self.objectCollection = append(self.objectCollection, obj)
	
	def setBackground(self, color):
		self.bg = color
	
	def setBackfaceCulling(self, value):
		self.backfaceCulling = value

Cube = Object(
	array([0,0,0]),		#position
	array([0,0,0]),		#rotation
	array([1,1,1]),		#scale
	array([				#vertex table
		[-1,-1,-1],			#0
		[-1,-1, 1],			#1
		[-1, 1,-1],			#2
		[-1, 1, 1],			#3
		[ 1,-1,-1],			#4
		[ 1,-1, 1],			#5
		[ 1, 1,-1],			#6
		[ 1, 1, 1]],		#7
		dtype=float),
	array([				#triangle table
		[ 0, 1, 2],			#0
		[ 1, 3, 2],			#1
		[ 0, 2, 4],			#2
		[ 2, 6, 4],			#3
		[ 4, 6, 7],			#4
		[ 4, 7, 5],			#5
		[ 0, 4, 1],			#6
		[ 4, 5, 1],			#7
		[ 2, 3, 7],			#8
		[ 2, 7, 6],			#9
		[ 1, 7, 3],			#10
		[ 1, 5, 7]])		#11
)

Pyramid = Object(
	array([0,0,0]),		#position
	array([0,0,0]),		#rotation
	array([1,1,1]),		#scale
	array([				#vertex table
		[-1,-1,-1],			#0
		[-1, 1,-1],			#1
		[ 1,-1,-1],			#2
		[ 1, 1,-1],			#3
		[ 0, 0, 1]],		#4
		dtype=float),
	array([				#triangle table
		[0,1,2],			#0
		[1,3,2],			#1
		[1,4,3],			#2
		[2,3,4],			#3
		[0,2,4],			#4
		[0,4,1]])			#5
)

Plane = Object(

	array([0,0,0]),		#position
	array([0,0,0]),		#rotation
	array([1,1,1]),		#scale
	array([				#vertex table
		[-1,-1, 0],			#0
		[-1, 1, 0],			#1
		[ 1,-1, 0],			#2
		[ 1, 1, 0]],		#3
		dtype=float),
	array([				#surface table
		[0,2,1],			#0
		[1,2,3]])		    #1
)

def LoadObjectfromOBJ(filename):

	vertexTable = array([])
	triTable = array([])

	file = open(filename, 'r')
	
	for line in file:
		tempLine = line
		if line[0] == "v":
			tempLine = tempLine.replace("\n", "")
			tempLine = tempLine.replace("v ", "")
			tempLine = tempLine.split()
			tempLine = [float(value) for value in tempLine]
			vertexTable = append(vertexTable, tempLine)
		if line[0] == "f":
			tempLine = tempLine.replace("\n", "")
			tempLine = tempLine.replace("f ", "")
			tempLine = tempLine.split()
			tempLine = [int(value) for value in tempLine]
			triTable = append(triTable, tempLine - array([1,1,1]))

	vertexTable = reshape(vertexTable, (int(len(vertexTable)/3), 3))
	triTable = reshape(triTable, (int(len(triTable)/3), 3))
	
	file.close()

	loadedObject = Object(
		array([0,0,0]),		#position
		array([0,0,0]),		#rotation
		array([1,1,1]),		#scale
		vertexTable,
		triTable
	)

	return loadedObject

Sphere = LoadObjectfromOBJ("uvsphere.obj")

Suzanne = LoadObjectfromOBJ("suzanne.obj")

Dodeca = LoadObjectfromOBJ("Dodecahedron.obj")

Igloo = LoadObjectfromOBJ("igloo.obj")

Axis = LoadObjectfromOBJ("axis.obj")

Grid = LoadObjectfromOBJ("grid.obj")