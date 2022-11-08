from functiondef import *
import pygame as pg
from numpy import *

def main():

	screen = Screen(1000,500)


	pg.init()
	pg.display.set_icon(pg.image.load("widechora.png"))
	pg.display.set_caption("RTX 500000 RAYTRACED 16K GAMING")
	pgscreen = pg.display.set_mode(screen.res)
	
	cam = Camera()
	cam.setPos(array([0, 0, 0]))
	cam.setRot(array([0, 0, 0]))

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

if __name__=="__main__":
	main()