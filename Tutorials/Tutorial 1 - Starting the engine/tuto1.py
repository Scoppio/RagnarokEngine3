from RagnarokEngine3.RE3 import Ragnarok, Vector2

engine = Ragnarok(Vector2(640, 480), "RAGNAROK TUTORIAL 1")

world = engine.get_world()
world.clear_color = (255, 255, 255)

engine.run()