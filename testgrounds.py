from numpy import *

def display(array):
    lineString = ""
    for line in array:
        lineString = ""
        for pixel in line:
            lineString = lineString + str(pixel) + " "
        print(lineString)

def drawLine(point0, point1):
    x0,y0 = point0
    x1,y1 = point1

    



screen = full((50, 50), 0)
display(screen)