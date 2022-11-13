from functiondef import *
import pygame as pg
from numpy import *

def main():

	screen = Screen(1000,500)


	pg.init()
	pg.display.set_icon(pg.image.load("icon32.png"))
	pg.display.set_caption("Butane 0.1")
	pgscreen = pg.display.set_mode(screen.res)
	
	cam = Camera()
	cam.setPosition(array([0, 0, -3.6]))
	cam.setRotation(array([0, 0, 0]))

	for vertex in Cube.wldSpaceVertexTable:
		projectedVertex = project(vertex, cam, screen)
		screen.drawPixel(projectedVertex, white)
		print(projectedVertex)



	running = True
	# display loop
	while running:
		pg.surfarray.blit_array(pgscreen, screen.pixels)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
		pg.display.update()

if __name__ == "__main__":
	main()