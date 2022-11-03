import pygame as pg
from numpy import *

class Object:
	def __init__(self, position, rotation, scale, vertexTable, edgeTable, surfaceTable):
		self.pos = position
		self.rot = rotation
		self.scl = scale

		self.vertexTable = vertexTable
		self.edgeTable = edgeTable
		self.surfaceTable = surfaceTable

	def applyPosition(self):
		for vertex in self.vertexTable:
			vertex = translateVertex(vertex, self.pos)
		self.pos = array([0, 0, 0])
	
	def applyRotation(self):
		for vertex in self.vertexTable:
			vertex = rotateVertex(vertex, self.pos, self.rot)
		self.rot = array([0, 0, 0])
	
	def applyScale(self):
		for vertex in self.vertexTable:
			vertex = scaleVertex(vertex, self.pos, self.scl)
		self.scl = array([0, 0, 0])
	
	def projectAll(self, camera):
		projectedVertexTable = zeros((len(self.vertexTable), 2))
		for i in range(len(self.vertexTable)):
			projectedVertexTable[i] = project(self.vertexTable[i], camera)
		return projectedVertexTable


class Empty:
	def __init__(self, position = array([0,0,0]), rotation = array([0,0,0]), scale = array([0,0,0])):
		self.pos = position
		self.rot = rotation
		self.scl = scale

class Camera:
	def __init__(self, position = array([0,0,0]), rotation = array([0,0,0]), scale = array([0,0,0]), focalLength = 1, shiftX = 0, shiftY = 0):
		self.pos = position
		self.rot = rotation
		self.scl = scale
		self.fL = focalLength
		self.sX = shiftX
		self.sY = shiftY

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
	return ((vertex-origin)*scl)+origin

def project(vertex, camera):

	rotatedVertex = rotateVertex(vertex, camera.pos, camera.rot)	#transform into camera space

	projectedX = ( ( camera.fL / rotatedVertex[2] ) * rotatedVertex[0] ) + camera.sX	#project onto view plane
	projectedY = ( ( camera.fL / rotatedVertex[2] ) * rotatedVertex[1] ) + camera.sY	#project onto view plane

	return array([projectedX, projectedY])


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
		[14,15,17],			#11
	])
)