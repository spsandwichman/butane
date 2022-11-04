from functiondef import *
import pygame as pg
from numpy import *

def main():

	resolution = (1000,500)
	width, height = resolution
	screen = full((width,height,3), 0, dtype=uint8)


	pg.init()
	pg.display.set_icon(pg.image.load("widechora.png"))
	pg.display.set_caption("RTX 500000 RAYTRACED 16K GAMING")
	pgscreen = pg.display.set_mode(resolution)
	

	camera = Camera()
	












	running = True
	# display loop
	while running:
		pg.surfarray.blit_array(pgscreen, screen)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
		pg.display.update()

if __name__=="__main__":
	main()