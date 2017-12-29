from RagnarokEngine3.RE3 import Vector2, Ragnarok, Sprite

engine = Ragnarok(Vector2(640, 480), "RAGNAROK TUTORIAL 1")

world = engine.get_world()
world.clear_color = (255, 255, 255)

sprite = Sprite()

sprite.update_order = 0
sprite.draw_order = 0
sprite.load_texture("Ragnarok.jpg")

# sprite.scale(Vector2(0.5, 0.5))
# sprite.coord=R.Vector2(0,0) # in the center of screen

world.add_obj(sprite)

engine.run()
