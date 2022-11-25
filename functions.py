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

def translateVector(vector, trn):
	translationMatrix = array([
		[1, 0, 0, trn[0]],
		[0, 1, 0, trn[1]],
		[0, 0, 1, trn[2]],
		[0, 0, 0, 1]])
	
	return delete((translationMatrix @ append(vector,1).T).T,3)

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
	rotationMatrix = xRotMatrix @ yRotMatrix @ zRotMatrix #compound rotation matrix

	return delete((rotationMatrix @ append((vector-origin),1).T).T,3)+origin

def scaleVector(vector, scl, origin = array([0,0,0])): 
	scaleMatrix = array([
		[scl[0], 0, 0, 0],
		[0, scl[1], 0, 0],
		[0, 0, scl[2], 0],
		[0, 0, 0, 1]])
	
	return delete((scaleMatrix @ append((vector-origin),1).T).T,3)+origin

def clipSpace(vertex, camera, screen):

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
	RotMatrix = xRotMatrix @ yRotMatrix @ zRotMatrix #compound rotation matrix

	camSpaceVertex = RotMatrix @ append((vertex-camera.pos),1) #transform into camera space

	projectionMatrix = array([
		[1/(tan(camera.FOV/2)), 0, 0, 0],
		[0, 1/(tan(camera.FOV/2)/screen.aspectRatio), 0, 0],
		[0, 0, ((-camera.nearZ-camera.farZ)/camera.nearZ-camera.farZ), ((2*camera.nearZ*camera.farZ)/camera.nearZ-camera.farZ)],
		[0, 0, 1, 0]
	])

	return matmul(camSpaceVertex, projectionMatrix)

def imageSpace(clipSpaceVertex, camera, screen):

	return array([(clipSpaceVertex[0]/clipSpaceVertex[3]+camera.sX),(clipSpaceVertex[1]/clipSpaceVertex[3]+camera.sY)])

def screenSpace(imageSpaceVertex, screen):
	projectedX = (imageSpaceVertex[0]+1)*(screen.width/2)
	projectedY = (imageSpaceVertex[1]+1)*(screen.height/2)

	return array([(imageSpaceVertex[0]+1)*(screen.width/2),(imageSpaceVertex[1]+1)*(screen.height/2)], dtype=int)