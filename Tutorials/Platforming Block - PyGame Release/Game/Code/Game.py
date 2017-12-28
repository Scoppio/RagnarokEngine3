import Ragnarok as r
import random
import Screens
import LevelData
import TileHeroCharacter
import DataParser

class Game(object):
    """
    Game acts as the entry point into Platforming Block.
    It prepares all the tile maps for loading and starts the first level.
    """
    def __init__(self):
        self.level_manager = LevelData.LevelProgressionManager()

        """
        tile_bindings is used to give our tiles a meaning.
        Each TileMap must be presented with a BindingType dictionary in order to understand what a number in a tilemap file means.

        For example, we could create a dictionary that includes {"0", ["Solid"]}, {"1", ["Solid", "Damage"] }
        When our tilemap parses in a file that contains a 0, that tile will have a binding_type of "Solid"
        When our tilemap parses in a 1, that tile will have a binding_type of "Solid" and "Damage"

        It is up to you to give these tiles meaning in your game.
        """
        tile_bindings = {}
        tile_bindings["0"] = ["Passthrough"]
        tile_bindings["1"] = ["Solid"]
        tile_bindings["2"] = ["Hazard"]
        tile_bindings["3"] = ["Warp"]
        tile_bindings["r"] = ["Reload"]

        #Load all of our levels. MapCount is the number of levels we need to load. (Levels start at index 0.)
        mapCount = 8
        for i in range(mapCount):
            data_path = "..//Maps//Level" + str(i) + "//Data.txt"
            dta = DataParser.parse(data_path)
            prefix = "..//Maps//Level" + str(i) + "//Lv" + str(i)
            tile_path = prefix + "_TileMap.txt"
            collision_path = prefix + "_CollisionMap.txt"
            object_path = prefix + "_ObjectMap.txt"
            level = "Level " + str(i)
            self.level_manager.levels.append(level)
            tile_map = r.SpriteSheet()
            tile_map.load_texture("..//Textures//" + dta[0], cell_size = r.Vector2(16, 16))
            _map = r.TileMap(tile_map, tile_bindings, tile_path, collision_path, object_path, LevelData.ObjAry, level)
            r.TileMapManager.add_map(_map)

        #Change this variable to the level you want to test.
        level_test = 0
        self.level_manager.current_level = (level_test - 1)
        self.level_manager.load_next_level()

        #Prepare our hero tile for use.
        self.hero = LevelData.load_character(r.TileMapManager.active_map, self)
        self.hero.set_default_pos(r.TileMapManager.active_map.start_location)
        r.Ragnarok.get_world().add_obj(self.hero)
