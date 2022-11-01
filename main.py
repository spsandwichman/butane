from turtle import width
from functiondef import *
import pygame as pg
 
def main():
    
    pg.init()
    pg.display.set_icon(pg.image.load("widechora.png"))
    pg.display.set_caption("RTX 500000 RAYTRACED 16K GAMING")
    screen = pg.display.set_mode((1000,500))
     
    running = True
    
    # Cube = cObject()

    # main loop
    while running:
        width, height = pg.display.get_window_size()

        # event handling, gets all event from the event queue
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                running = False
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()