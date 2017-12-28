import Ragnarok as r
import Screens
import TileHeroCharacter as thc

def hazard_touched_method(hero):
    screen = Screens.LoseScreen(hero)
    screen.show()
    screen.draw_order = 15000
    r.Ragnarok.get_world().add_obj(screen)

def special_touched_method():
    hero.CURRENT_STATE = hero.PAUSED_STATE
    screen = Screens.WinScreen()
    screen.show()
    screen.draw_order = 15000
    r.Ragnarok.get_world().add_obj(screen)

def load_character(tile_map, gamescreen):
    """Create an instance of the main character and return it."""
    tile_obj = thc.TileHeroCharacter(tile_map, gamescreen)
    tile_obj.load_texture("..//Textures//character.png")
    tile_obj.origin = r.Vector2(0, 0)
    tile_obj.hazard_touched_method = hazard_touched_method
    tile_obj.special_touched_method = special_touched_method
    return tile_obj

#Object array is a master array containing all the objects the user may want to place on a map.
ObjAry = []

text_360 = None
twitter = None
fb = None
fb2 = None
def create_text():
    text_360 = r.Text(110, 110, Screens.font_path, 24, (0, 0, 0))
    text_360.text = "Platforming Block is coming to the XBox 360!"
    text_360.coords = r.Vector2(425, 140)
    text_360.tag = "Final Screen Text"

    twitter = r.Text(110, 110, Screens.font_path, 24, (0, 0, 0))
    twitter.text = "Follow us on Twitter: @LotusGames"
    twitter.coords = r.Vector2(425, 480)
    twitter.tag = "Final Screen Text"

    fb = r.Text(110, 110, Screens.font_path, 24, (0, 0, 0))
    fb.text = "Join the Platforming Block FaceBook page:"
    fb.coords = r.Vector2(425, 520)
    fb.tag = "Final Screen Text"

    fb2 = r.Text(110, 110, Screens.font_path, 16, (0, 0, 0))
    fb2.text = "www.facebook.com/pages/Platforming-Block/123334587706222"
    fb2.coords = r.Vector2(425, 540)
    fb2.tag = "Final Screen Text"

    r.Ragnarok.get_world().add_obj(text_360)
    r.Ragnarok.get_world().add_obj(twitter)
    r.Ragnarok.get_world().add_obj(fb)
    r.Ragnarok.get_world().add_obj(fb2)

def destroy_text():
    r.Ragnarok.get_world().remove_all("Final Screen Text")

class LevelProgressionManager(object):
    def __init__(self):
        self.levels = []
        self.current_level = -1

    def load_next_level(self):
        self.current_level += 1
        if self.current_level > len(self.levels) - 1:
            self.current_level = 0

        #Create the text objects for the last level.
        if self.current_level == 7:
            create_text()
        else:
            destroy_text()

        r.TileMapManager.load(self.levels[self.current_level])

    def load_previous_level(self):
        self.current_level += 1
        r.TileMapManager.load(self.levels[self.current_level])