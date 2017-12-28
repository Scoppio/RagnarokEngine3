class Key(r.TileMapObject):
    def __init__(self, character, tileMap, winFunction):
        super(Key, self).__init__(tileMap)
        self.load_texture("power_up.png")
        self.origin = r.Vector2(0, 0)
        self.char = character
        self.win_function = winFunction

    def check_player_collision(self):
        """Check to see if we are colliding with the player."""
        player_tiles = r.TileMapManager.active_map.grab_collisions(self.char.coords)
        enemy_tiles = r.TileMapManager.active_map.grab_collisions(self.coords)

        #Check to see if any of the tiles are the same. If so, there is a collision.
        for ptile in player_tiles:
            for etile in enemy_tiles:
                if r.TileMapManager.active_map.pixels_to_tiles(ptile.coords) == r.TileMapManager.active_map.pixels_to_tiles(etile.coords):
                    return True

        return False

    def update(self, milliseconds):
        if self.check_player_collision():
            self.win_function()
            r.Ragnarok.get_world().remove_obj(self)