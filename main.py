from classes import * # imports numpy and functions.py through reference
import pygame as pg

def main():

	screen = Screen(1000,1000)
	scene = Scene()
	
	pg.init()
	pg.display.set_icon(pg.image.load("icon32.png"))
	pg.display.set_caption("Butane 0.1")
	pgscreen = pg.display.set_mode(screen.res)

	clock = pg.time.Clock()

	cam = Camera()
	cam.setPosition(array([-1.5, 6, 1]))
	cam.setRotation(array([r(-90), 0, 0]))

	Cube.setPosition(array([1.5, 0, 0]))
	Pyramid.setPosition(array([-1.5, 0, 0]))

	Plane.setPosition(array([0, 0, -1]))
	Plane.setScale(array([4,4,4])) 

	scene.addObjectToScene(Cube)
	scene.addObjectToScene(Pyramid)
	#scene.addObjectToScene(Plane)


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


		#SCENE RENDERING
		for obj in scene.objectCollection:
			obj.projectAll(cam, screen)
			for edge in obj.edgeTable:
				screen.drawLine(obj.projectedVertexTable[edge[0]], obj.projectedVertexTable[edge[1]], white)
			for vertex in obj.projectedVertexTable:
				screen.drawPixel(vertex, red)
		
		Cube.rotate(array([0,0,-0.01]))
		Pyramid.rotate(array([0,0,0.03]))
	
		#Pyramid.scale(array([1,1.01,1]))
		

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
					cam.rotate(array([r(-10), 0, 0]))
				if event.key == pg.K_DOWN:
					cam.rotate(array([r(10), 0, 0]))
				if event.key == pg.K_LEFT:
					cam.rotate(array([0, 0, r(10)]))
				if event.key == pg.K_RIGHT:
					cam.rotate(array([0, 0, r(-10)]))
		
		
		screen.clear()
		pg.display.update()
		

		clock.tick()
		#print("fps: " + str(int(clock.get_fps())))
		print("cam pos: " + str(cam.pos) +  " cam rot: " + str(cam.rotDeg) + " fps: " + str(int(clock.get_fps())))
		



if __name__ == "__main__":
	main()