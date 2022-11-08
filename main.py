from functiondef import *
import pygame as pg
from numpy import *

def main():

	screen = Screen(1000,500)


	pg.init()
	pg.display.set_icon(pg.image.load("widechora.png"))
	pg.display.set_caption("RTX 500000 RAYTRACED 16K GAMING")
	pgscreen = pg.display.set_mode(screen.res)
	
	
	screen.drawLine((10,10),(700,365), red)



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