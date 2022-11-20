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
	cam.setRotation(array([r(0), r(0), r(0)]))





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

		Cube.projectAll(cam, screen)
		for edge in Cube.edgeTable:
			screen.drawLine(Cube.projectedVertexTable[edge[0]], Cube.projectedVertexTable[edge[1]], white)
		for vertex in Cube.projectedVertexTable:
			screen.drawPixel(vertex, red)
		Cube.setScale(array([1, 1, 1]))
		#Cube.rotate(array([0.0, 0.002, 0.005]))
		
		
		pg.surfarray.blit_array(pgscreen, screen.pixels)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False
				if event.key == pg.K_w:
					cam.translate(array([0, 0, -0.5]))
				if event.key == pg.K_s:
					cam.translate(array([0, 0, 0.5]))
				if event.key == pg.K_a:
					cam.translate(array([0.5, 0, 0]))
				if event.key == pg.K_d:
					cam.translate(array([-0.5, 0, 0]))
				if event.key == pg.K_LSHIFT:
					cam.translate(array([0, 0.5, 0]))
				if event.key == pg.K_SPACE:
					cam.translate(array([0, -0.5, 0]))
				if event.key == pg.K_UP:
					cam.rotate(array([r(-1), 0, 0]))
				if event.key == pg.K_DOWN:
					cam.rotate(array([r(1), 0, 0]))
		
		
		screen.clear()
		pg.display.update()

		clock.tick()
		#print("fps: " + str(int(clock.get_fps())))
		print(str(cam.pos) + str(cam.rot))
		



if __name__ == "__main__":
	main()