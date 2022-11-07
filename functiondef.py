import pygame as pg
from numpy import *

white = array([255,255,255])
black = array([0,0,0])
red = array([255,0,0])
green = array([0,255,0])
blue = array([0,0,255])


class Object:
	def __init__(self, position, rotation, scale, vertexTable, edgeTable, surfaceTable): 
		self.pos = position
		self.rot = rotation
		self.scl = scale

		self.objectVertexTable = vertexTable
		self.WorldVertexTable = vertexTable
		self.edgeTable = edgeTable
		self.surfaceTable = surfaceTable

	

class Empty:
	def __init__(self, position = array([0,0,0]), rotation = array([0,0,0]), scale = array([1,1,1])):
		self.pos = position
		self.rot = rotation
		self.scl = scale

class Camera:
	def __init__(self, position = array([0,0,0]), rotation = array([0,0,0]), scale = array([1,1,1]), focalLength = 10, shiftX = 0, shiftY = 0):
		self.pos = position
		self.rot = rotation
		self.scl = scale
		self.fL = focalLength
		self.sX = shiftX
		self.sY = shiftY

class Screen:
	def __init__(self, height, width):
		self.pixels = full((width,height,3), 0, dtype=uint8)
		self.res = (height, width)
		self.resolution = (height, width)
		self.h = height
		self.height = height
		self.w = width
		self.width = width

def translateVertex(vertex, trn):
	return vertex+trn

def rotateVertex(vertex, origin, rot):

	xRotMatrix = array([
		[1,            0,           0], # x-axis rotation matrix
		[0,  cos(rot[0]), sin(rot[0])],
		[0, -sin(rot[0]), cos(rot[0])],
	])
	yRotMatrix = array([
		[cos(rot[1]), 0, -sin(rot[1])], # y-axis rotation matrix
		[          0, 1,            0],
		[sin(rot[1]), 0,  cos(rot[1])],
	])
	zRotMatrix = array([
		[ cos(rot[2]), sin(rot[2]), 0], # z-axis rotation matrix
		[-sin(rot[2]), cos(rot[2]), 0],
		[           0,           0, 1],
	])
	RotMatrix = matmul(matmul(xRotMatrix, yRotMatrix), zRotMatrix) #compound rotation matrix

	return (matmul((vertex - origin).T, RotMatrix).T) + origin # magic

def scaleVertex(vertex, origin, scl): 
	return ((vertex - origin) * scl) + origin

def project(vertex, camera, screen):

	rotatedVertex = rotateVertex(vertex, camera.pos, camera.rot)	#transform into camera space

	projectedX = ( ( camera.fL / rotatedVertex[2] ) * rotatedVertex[0] ) + camera.sX	#project onto view plane
	projectedY = ( ( camera.fL / rotatedVertex[2] ) * rotatedVertex[1] ) + camera.sY	#project onto view plane

	projectedX = (projectedX*10) + (screen.width/2)
	projectedY = (projectedY*10) + (screen.height/2)

	return array([projectedX, projectedY], int32)

def projectAll(vertexTable, camera):
		projectedVertexTable = zeros((len(vertexTable), 2), int32)
		for i in range(len(vertexTable)):
			projectedVertexTable[i] = project(vertexTable[i], camera)
		return projectedVertexTable


def drawLine(point0, point1, screen): #bresenham magic
	x0, y0 = point0[0], point0[1]
	x1, y1 = point1[0], point1[1]
	dx = abs( x1 - x0)
	sx = 1 if x0 < x1 else -1
	dy = -abs(y1 - y0)
	sy = 1 if y0 < x1 else -1
	error = dx + dy
	while True:
		screen.pixels[x0][y0] = white
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
		[ 1, 1, 1]]),		#7
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
		[ 0, 0, 1]]),		#4
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