from functiondef import *
import pygame as pg
from numpy import *

def main():

	screen = Screen(1000,500)


	pg.init()
	pg.display.set_icon(pg.image.load("icon32.png"))
	pg.display.set_caption("Butane 0.1")
	pgscreen = pg.display.set_mode(screen.res)

	clock = pg.time.Clock()

	cam = Camera()
	cam.setPosition(array([0, 0, 5]))
	cam.setRotation(array([0, 0, 0]))
	Pyramid.setRotation(array([r(-90), 0.0, 0.0]))





	running = True
	# display loop

	while running:
		
		Pyramid.projectAll(cam, screen)

		for edge in Pyramid.edgeTable:
			screen.drawLine(Pyramid.projectedVertexTable[edge[0]], Pyramid.projectedVertexTable[edge[1]], white)

		for vertex in Pyramid.projectedVertexTable:
			screen.drawPixel(vertex, red)
		
		Pyramid.setRotation(array([0.0, 0.01, 0.0]))
		print(Pyramid.rot)
		
		pg.surfarray.blit_array(pgscreen, screen.pixels)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False
		
		screen.clear()
		pg.display.update()

		clock.tick()
		print(clock.get_fps())
		



if __name__ == "__main__":
	main()