from turtle import width
from functiondef import *
import pygame as pg
 
def main():
    
    pg.init()
    pg.display.set_icon(pg.image.load("widechora.png"))
    pg.display.set_caption("RTX 500000 RAYTRACED 16K GAMING")
    screen = pg.display.set_mode((1000,500))
    width, height = pg.display.get_window_size()
    def sw(coord):
        return coord*width 
    def sh(coord):
        return coord*height


    running = True
    
    

    # main loop
    while running:
        width, height = pg.display.get_window_size()

        # event handling, gets all event from the event queue
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                running = False
     
     





if __name__=="__main__":
    main()