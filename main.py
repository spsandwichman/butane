from functiondef import *
import pygame as pg
import numpy as np
 
def main():

    pg.init()
    pg.display.set_icon(pg.image.load("widechora.png"))
    pg.display.set_caption("RTX 500000 RAYTRACED 16K GAMING")
    screen = pg.display.set_mode((1000,500), pg.RESIZABLE)
    width, height = pg.display.get_window_size()

    camera = Camera()
    

    def w(coord):
        return int(coord*width)
    def h(coord):
        return int(coord*height)


    running = True
    
    

    # main loop
    while running:
        screen.fill((10,10,10))
        width, height = pg.display.get_window_size()









        # event handling, gets all event from the event queue
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                running = False

        pg.display.update()


if __name__=="__main__":
    main()