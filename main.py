from classes import * # imports numpy and functions.py through reference
import pygame as pg

def main():

	screen = Screen(1000,500)
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

	Igloo.setScale(array([3,3,3]))

	scene.addObjectToScene(Plane)
	#scene.addObjectToScene(Cube)
	#scene.addObjectToScene(Pyramid)
	scene.addObjectToScene(Igloo)
	scene.setBackground(array([10,10,10]))
	#scene.setBackfaceCulling(False)


	running = True
	# display loop
	while running:

		#SCENE RENDERING PIPELINE - TRIANGLE BY TRIANGLE
		for obj in scene.objectCollection:
			for tri in obj.triTable:
				v0 = obj.wldSpaceVertexTable[int(tri[0])].copy()
				v1 = obj.wldSpaceVertexTable[int(tri[1])].copy()
				v2 = obj.wldSpaceVertexTable[int(tri[2])].copy()

				normalVector = cross((v0-v1),(v1-v2)) / linalg.norm(cross((v0-v1),(v1-v2))) # calculates normal vector from normalized cross product
				averagePosition = array([(v0[0]+v1[0]+v2[0])/3,(v0[1]+v1[1]+v2[1])/3,(v0[2]+v1[2]+v2[2])/3]) # mean position of all points in triangle
				cameraToTriangleVector = averagePosition - cam.pos
				
				if scene.backfaceCulling and (dot(normalVector, cameraToTriangleVector) >= 0):
					continue # skip over any triangles that are not facing the camera
				
				clipSpaceV0 = clipSpace(v0, cam, screen)
				clipSpaceV1 = clipSpace(v1, cam, screen)
				clipSpaceV2 = clipSpace(v2, cam, screen)


				imageSpaceV0 = imageSpace(clipSpaceV0, cam, screen)
				imageSpaceV1 = imageSpace(clipSpaceV1, cam, screen)
				imageSpaceV2 = imageSpace(clipSpaceV2, cam, screen)

				screenSpaceV0 = screenSpace(imageSpaceV0, screen)
				screenSpaceV1 = screenSpace(imageSpaceV1, screen)
				screenSpaceV2 = screenSpace(imageSpaceV2, screen)

				screen.drawLine(screenSpaceV0, screenSpaceV1, white)
				screen.drawLine(screenSpaceV1, screenSpaceV2, white)
				screen.drawLine(screenSpaceV2, screenSpaceV0, white)
				#screen.drawTriangle(screenSpaceV0, screenSpaceV1, screenSpaceV2, white)







		Cube.rotate(array([0,0,-0.01]))
		Pyramid.rotate(array([0,0,0.03]))
		Igloo.rotate(array([0,0,0.03]))


		pg.surfarray.blit_array(pgscreen, screen.pixels)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False
				if event.key == pg.K_w:
					cam.translate(array([0, 0, 0.5]))
				if event.key == pg.K_s:
					cam.translate(array([0, 0, -0.5]))
				if event.key == pg.K_a:
					cam.translate(array([0.5, 0, 0]))
				if event.key == pg.K_d:
					cam.translate(array([-0.5, 0, 0]))
				if event.key == pg.K_LSHIFT:
					cam.translate(array([0, 0.5, 0]))
				if event.key == pg.K_SPACE:
					cam.translate(array([0, -0.5, 0]))
				if event.key == pg.K_UP:
					cam.rotate(array([r(-5), 0, 0]))
				if event.key == pg.K_DOWN:
					cam.rotate(array([r(5), 0, 0]))
				if event.key == pg.K_LEFT:
					cam.rotate(array([0, 0, r(5)]))
				if event.key == pg.K_RIGHT:
					cam.rotate(array([0, 0, r(-5)]))


		# screen.fill(scene.bg)
		screen.clear()
		pg.display.update()


		clock.tick()
		#print("fps: " + str(int(clock.get_fps())))
		print("cam pos: " + str(cam.pos) +  " cam rot: " + str(cam.rotDeg) + " fps: " + str(int(clock.get_fps())))




if __name__ == "__main__":
	main()