from numpy import *

def display(array):
    lineString = ""
    for line in array:
        lineString = ""
        for pixel in line:
            lineString = lineString + str(pixel) + " "
        print(lineString)

def plotLine(x0, y0, x1, y1, screen):
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy
    
    while True:
        screen[x0][y0] = 1
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

screen = full((50, 50), 0)

plotLine(1, 10, 49, 7, screen)

display(screen)