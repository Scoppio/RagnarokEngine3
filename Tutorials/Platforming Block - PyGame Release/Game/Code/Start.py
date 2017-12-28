#Platforming Block copyright Lotus Games
#Code by Clinton Myers
#Maps and graphics by Greg Frasier and Clinton Myers

import Ragnarok as r
import pygame
import Game as g

#Create an instance of the Ragnarok engine.
engine = r.Ragnarok(r.Vector2(800, 600), "Platformin' Block")

#The world is the entity where every object is stored.
#It automatically sorts our objects by update and draw order, and then updates and draws them for us.
world = engine.get_world()

#Create an instance of our game, which will add components necessary to gameplay to the Ragnarok engine.
game = g.Game()

#Set a few start up properties
pygame.mouse.set_visible(False)
engine.preferred_fps = 60
engine.print_frames = False

#Start the game loop.
engine.run()
