from numpy import *

white = array([255, 255, 255])
black = array([0, 0, 0])
red = array([255, 0, 0])
green = array([0, 255, 0])
blue = array([0, 0, 255])

def r(oldDegrees):
	return deg2rad(oldDegrees)

def d(oldRadians):
	return rad2deg(oldRadians)

class Object:
	def __init__(self, position, rotation, scale, objSpaceVertexTable, edgeTable, surfaceTable):
		self.pos = position
		self.rot = rotation				#always in radians
		self.rotDeg = rotation
		self.scl = scale

		self.objSpaceVertexTable = objSpaceVertexTable.copy()
		self.wldSpaceVertexTable = full((len(objSpaceVertexTable), 3), 0, dtype=float)
		self.projectedVertexTable = full((len(objSpaceVertexTable), 2), 0)
		self.edgeTable = edgeTable.copy()
		self.surfaceTable = surfaceTable.copy()
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

		rotationMatrix = matmul(matmul(xRotMatrix, yRotMatrix), zRotMatrix) #compound rotation matrix

		scaleMatrix = array([
		[self.scl[0], 0, 0, 0],
		[0, self.scl[1], 0, 0],
		[0, 0, self.scl[2], 0],
		[0, 0, 0, 1]])

		transformationMatrix = matmul(matmul(translationMatrix, rotationMatrix), scaleMatrix)

		for vertex in range(len(self.objSpaceVertexTable)):
			self.wldSpaceVertexTable[vertex] = delete(matmul(transformationMatrix,append(self.objSpaceVertexTable[vertex],1).T).T,3)
	
	def projectAll(self, camera, screen):
		for vertex in range(len(self.wldSpaceVertexTable)):
			self.projectedVertexTable[vertex] = project(self.wldSpaceVertexTable[vertex], camera, screen)
			
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

class Screen:
	def __init__(self, width, height):
		self.pixels = full((width, height, 3), 0, dtype=uint8)
		self.res = (width, height)
		self.height = height
		self.width = width
		self.aspectRatio = width/height
	
	def setResolution(self, newWidth, newHeight):
		self.height = newHeight
		self.width = newWidth
		self.res = (newWidth, newHeight)
		self.aspectRatio = newWidth/newHeight
	
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
			if (x0 >= self.width or y0 >= self.height) or (x0 < 0 or y0 < 0): #if i try to draw off the screen array, just /dont/
				return
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
		
	def fill(self, color):
		for row in range(self.width):
			for column in range(self.height):
				self.drawPixel((row, column), color)
	
	def clear(self):
		self.pixels = full((self.width, self.height, 3), 0, dtype=uint8)

class Scene:
	def __init__(self, backgroundColor = array([0,0,0])):
		self.objectCollection = empty(0, dtype=Object)
		self.bg = backgroundColor

	def addObjectToScene(self, obj):
		self.objectCollection = append(self.objectCollection, obj)




def translateVector(vector, trn):
	translationMatrix = array([
		[1, 0, 0, trn[0]],
		[0, 1, 0, trn[1]],
		[0, 0, 1, trn[2]],
		[0, 0, 0, 1]])
	
	return delete(matmul(translationMatrix,append(vector,1).T).T,3)

def rotateVector(vector, rot, origin = array([0,0,0])):

	xRotMatrix = array([					# x-axis rotation matrix
		[1, 0, 0, 0],
		[0, cos(rot[0]), sin(rot[0]), 0],
		[0, -sin(rot[0]), cos(rot[0]), 0],
		[0, 0, 0, 1]
	])
	yRotMatrix = array([					# y-axis rotation matrix
		[cos(rot[1]), 0, -sin(rot[1]), 0],
		[0, 1, 0, 0],
		[sin(rot[1]), 0, cos(rot[1]), 0],
		[0, 0, 0, 1]
	])
	zRotMatrix = array([					# z-axis rotation matrix
		[cos(rot[2]), sin(rot[2]), 0, 0], 
		[-sin(rot[2]), cos(rot[2]), 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	rotationMatrix = matmul(matmul(xRotMatrix, yRotMatrix), zRotMatrix) #compound rotation matrix

	return delete(matmul(rotationMatrix,append((vector-origin),1).T).T,3)+origin

def scaleVector(vector, scl, origin = array([0,0,0])): 
	scaleMatrix = array([
		[scl[0], 0, 0, 0],
		[0, scl[1], 0, 0],
		[0, 0, scl[2], 0],
		[0, 0, 0, 1]])
	
	return delete(matmul(scaleMatrix,append((vector-origin),1).T).T,3)+origin

def project(vertex, camera, screen):

	xRotMatrix = array([					# x-axis rotation matrix
		[1, 0, 0, 0],
		[0, cos(camera.rot[0]), sin(camera.rot[0]), 0],
		[0, -sin(camera.rot[0]), cos(camera.rot[0]), 0],
		[0, 0, 0, 1]
	])
	yRotMatrix = array([					# y-axis rotation matrix
		[cos(camera.rot[1]), 0, -sin(camera.rot[1]), 0],
		[0, 1, 0, 0],
		[sin(camera.rot[1]), 0, cos(camera.rot[1]), 0],
		[0, 0, 0, 1]
	])
	zRotMatrix = array([					# z-axis rotation matrix
		[cos(camera.rot[2]), sin(camera.rot[2]), 0, 0], 
		[-sin(camera.rot[2]), cos(camera.rot[2]), 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	RotMatrix = matmul(matmul(xRotMatrix, yRotMatrix), zRotMatrix) #compound rotation matrix

	camSpaceVertex = matmul(RotMatrix, append((vertex-camera.pos),1)) #transform into camera space

	projectionMatrix = array([
		[1/(tan(camera.FOV/2)), 0, 0, 0],
		[0, 1/(tan(camera.FOV/2)/screen.aspectRatio), 0, 0],
		[0, 0, ((-camera.nearZ-camera.farZ)/camera.nearZ-camera.farZ), ((2*camera.nearZ*camera.farZ)/camera.nearZ-camera.farZ)],
		[0, 0, 1, 0]
	])

	clipSpaceVertex = matmul(camSpaceVertex,projectionMatrix)

	#projectedX = clipSpaceVertex[0]/clipSpaceVertex[3]
	#projectedY = clipSpaceVertex[1]/clipSpaceVertex[3]

	projectedX = (clipSpaceVertex[0]/clipSpaceVertex[3]+1+camera.sX)*(screen.width/2)
	projectedY = (clipSpaceVertex[1]/clipSpaceVertex[3]+1+camera.sY)*(screen.height/2)

	return array([projectedX, projectedY], int32)

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
	array([      	   #edge table
		[0,1],				#0
		[0,2],				#1
		[0,4],				#2
		[1,2],				#3
		[1,3],				#4
		[1,4],				#5
		[1,5],				#6
		[1,7],				#7
		[2,3],				#8
		[2,4],				#9
		[2,6],				#10
		[2,7],				#11
		[3,7],				#12
		[4,5],				#13
		[4,6],				#14
		[4,7],				#15
		[5,7],				#16
		[6,7]]),			#17
	array([				#surface table
		[ 0, 1, 3],			#0
		[ 0, 2, 5],			#1
		[ 1, 2, 9],			#2
		[ 3, 7, 8],			#3
		[ 4, 7,12],			#4
		[ 6, 5,13],			#5
		[ 6, 7,16],			#6
		[ 8,11,12],			#7
		[ 9,10,14],			#8
		[10,11,17],			#9
		[13,15,16],			#10
		[14,15,17]])		#11
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
	array([				#edge table
		[0,1],				#0
		[0,2],				#1
		[0,3],				#2
		[0,4],				#3
		[1,3],				#4
		[1,4],				#5
		[2,3],				#6
		[2,4],				#7
		[3,4]]),			#8
	array([				#surface table
		[0,2,4],			#0
		[0,3,5],			#1
		[1,2,6],			#2
		[1,3,7],			#3
		[4,5,8],			#4
		[6,7,8]])			#5
)

