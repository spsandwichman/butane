import pygame as pg
import numpy as np

def translateVertex(vertex, trn):
	return vertex+trn

def rotateVertex(vertex, origin, rot):


	xRotMatrix = np.array([
		[1,               0,              0], # x-axis rotation matrix
		[0,  np.cos(rot[0]), np.sin(rot[0])],
		[0, -np.sin(rot[0]), np.cos(rot[0])],
	])
	yRotMatrix = np.array([
		[np.cos(rot[1]), 0, -np.sin(rot[1])], # y-axis rotation matrix
		[             0, 1,               0],
		[np.sin(rot[1]), 0,  np.cos(rot[1])],
	])
	zRotMatrix = np.array([
		[ np.cos(rot[2]), np.sin(rot[2]), 0], # z-axis rotation matrix
		[-np.sin(rot[2]), np.cos(rot[2]), 0],
		[              0,              0, 1],
	])
	RotMatrix = np.matmul(np.matmul(xRotMatrix, yRotMatrix), zRotMatrix) #compound rotation matrix

	return (np.matmul((vertex - origin).T, RotMatrix).T) + origin # magic

def scaleVertex(vertex, origin, scl): 
	return ((vertex-origin)*scl)+origin

def compoundProject(vertex, cameraPos, cameraRot, focalLength, shiftX=0, shiftY=0, ):

	rotatedVertex = rotateVertex(vertex, cameraPos, cameraRot)	#transform into camera space

	projectedX = ( ( focalLength / rotatedVertex[2] ) * rotatedVertex[0] ) + shiftX		#project onto view plane
	projectedY = ( ( focalLength / rotatedVertex[2] ) * rotatedVertex[1] ) + shiftY		#project onto view plane

	return np.array([projectedX, projectedY])

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
		self.pos = np.array([0, 0, 0])
	
	def applyRotation(self):
		for vertex in self.vertexTable:
			vertex = rotateVertex(vertex, self.pos, self.rot)
		self.rot = np.array([0, 0, 0])
	
	def applyScale(self):
		for vertex in self.vertexTable:
			vertex = scaleVertex(vertex, self.pos, self.scl)
		self.scl = np.array([0, 0, 0])

class Empty:
	def __init__(self, position = np.array([0,0,0]), rotation = np.array([0,0,0]), scale = np.array([0,0,0])):
		self.pos = position
		self.rot = rotation
		self.scl = scale

class Camera:
	def __init__(self, position = np.array([0,0,0]), rotation = np.array([0,0,0]), scale = np.array([0,0,0]), focalLength = 1, shiftX = 0, shiftY = 0):
		self.pos = position
		self.rot = rotation
		self.scl = scale
		self.fL = focalLength
		self.sX = shiftX
		self.sY = shiftY

Cube = Object(
	np.array([0,0,0]),	#position
	np.array([0,0,0]),	#rotation
	np.array([1,1,1]),	#scale
	np.array([			#vertex table
		[-1,-1,-1],			#0
		[-1,-1, 1],			#1
		[-1, 1,-1],			#2
		[-1, 1, 1],			#3
		[ 1,-1,-1],			#4
		[ 1,-1, 1],			#5
		[ 1, 1,-1],			#6
		[ 1, 1, 1]]),		#7
	np.array([         #edge table
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
	np.array([			#surface table
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