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
	cam.setPosition(array([0, 5, 5]))
	cam.setRotation(array([r(30), r(0), r(0)]))





	running = True
	# display loop

	while running:
		
		origin = project(array([0,0,0]), cam, screen)
		unitVectorX = project(array([1,0,0]), cam, screen)
		unitVectorY = project(array([0,1,0]), cam, screen)
		unitVectorZ = project(array([0,0,1]), cam, screen)

		screen.drawLine(unitVectorX, origin, red)
		screen.drawLine(unitVectorY, origin, green)
		screen.drawLine(unitVectorZ, origin, blue)
		screen.drawPixel(origin, white)

		Pyramid.projectAll(cam, screen)
		for edge in Pyramid.edgeTable:
			screen.drawLine(Pyramid.projectedVertexTable[edge[0]], Pyramid.projectedVertexTable[edge[1]], white)
		for vertex in Pyramid.projectedVertexTable:
			screen.drawPixel(vertex, red)
		Pyramid.rotate(array([0.0, 0.0, 0.005]))
		
		
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
		print("fps: " + str(int(clock.get_fps())))
		



if __name__ == "__main__":
	main()