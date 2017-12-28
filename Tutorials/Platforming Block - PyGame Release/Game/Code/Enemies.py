##import Ragnarok as r
##
##class Enemy(r.TileMapObject):
##    def __init__(self, character, tileMap, hazardTouchedMethod):
##        super(Enemy, self).__init__(tileMap)
##        self.move_speed = r.Vector2(100, 0.0)
##        rand = random.randrange(0, 2)
##        if rand == 0:
##            self.direction = -1
##        else:
##            self.direction = 1
##        self.timer = 0.0
##
##        #Used to see if we have collided with the main character.
##        self.char = character
##        self.load_texture("bad_block.png")
##        self.origin = r.Vector2.zero()
##        self.hazardTouchedMethod = hazardTouchedMethod
##
##    def check_player_collision(self):
##        """Check to see if we are colliding with the player."""
##        player_tiles = r.TileMapManager.active_map.grab_collisions(self.char.coords)
##        enemy_tiles = r.TileMapManager.active_map.grab_collisions(self.coords)
##
##        #Check to see if any of the tiles are the same. If so, there is a collision.
##        for ptile in player_tiles:
##            for etile in enemy_tiles:
##                if r.TileMapManager.active_map.pixels_to_tiles(ptile.coords) == r.TileMapManager.active_map.pixels_to_tiles(etile.coords):
##                    return True
##
##        return False
##
##    def update(self, milliseconds):
##        self.timer += milliseconds
##        if self.timer >= 2500:
##            self.direction *= -1
##            self.timer = 0.0
##        self.coords[0] += self.direction * self.move_speed[0] * (milliseconds / 1000.0)
##        if self.check_player_collision():
##            self.hazardTouchedMethod()