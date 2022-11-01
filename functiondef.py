import numpy as np

def rotate(vertex, origin, rot):

    xRotMatrix = np.mat([
        [1,               0,              0], # x-axis rotation matrix
        [0,  np.cos(rot[0]), np.sin(rot[0])],
        [0, -np.sin(rot[0]), np.cos(rot[0])],
    ])
    yRotMatrix = np.mat([
        [np.cos(rot[1]), 0, -np.sin(rot[1])], # y-axis rotation matrix
        [             0, 1,               0],
        [np.sin(rot[1]), 0,  np.cos(rot[1])],
    ])
    zRotMatrix = np.mat([
        [ np.cos(rot[2]), np.sin(rot[2]), 0], # z-axis rotation matrix
        [-np.sin(rot[2]), np.cos(rot[2]), 0],
        [              0,              0, 1],
    ])
    RotMatrix = np.matmul(np.matmul(xRotMatrix, yRotMatrix), zRotMatrix) #compound rotation matrix

    return (np.matmul((vertex - origin).T, RotMatrix).T) + origin # magic

def cProject(vertex, cameraPos, cameraRot, focalLength, shiftX=0, shiftY=0):

    rotatedVertex = rotate(vertex, cameraPos, cameraRot) # transform into camera space

    projectedX = ( ( focalLength / rotatedVertex[2] ) * rotatedVertex[0] ) + shiftX  #project onto view plane
    projectedY = ( ( focalLength / rotatedVertex[2] ) * rotatedVertex[1] ) + shiftY 

    return np.array([projectedX, projectedY])

class cObject:
    def __init__(self, position, rotation, scale, vertexTable, edgeTable, surfaceTable) -> None:
        self.pos = position
        self.rot = rotation
        self.scl = scale

        self.vertexTable = vertexTable
        self.edgeTable = edgeTable
        self.surfaceTable = surfaceTable