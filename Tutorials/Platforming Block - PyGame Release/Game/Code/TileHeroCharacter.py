import Ragnarok as r
import pygame
import math

class TileHeroCharacter(r.TileMapObject):
    """Provides some basic data and methods for a playable character in a tile map."""
    def __init__(self, tileMap, GameScreen):
        """
        Create a basic character that can move around the tile world.
        tileMap is a reference to the tile map that this object is associated with.
        """
        super(TileHeroCharacter, self).__init__(tileMap)
        self.game_screen = GameScreen
        self.desired_position = r.Vector2(100, 20)
        self.JUMPING_STATE = "JUMPING"
        self.NORMAL_STATE = "NORMAL"
        self.is_paused = False
        self.CURRENT_STATE = self.NORMAL_STATE
        self.draw_order = 5000

        #The number of blocks our character can jump.
        #Everything is in pixels per second.
        block_jump_height = 6
        tile_height = 16
        fall_acceleration= 8 * tile_height

        #Based off equation: -vi = sqrt( 2 * acceleration * delta y )
        self.jump_velocity = math.sqrt(2 * (fall_acceleration) * (block_jump_height * tile_height))
        self.run_speed = 145

        #The method that runs when a hazard tile is touched.
        self.hazard_touched_method = None

        self.bounding_box = r.AABoundingBox()
        self.bounding_box = pygame.Rect(0, 0, 100, 100)
        self.velocity = r.Vector2()
        self.acceleration = r.Vector2(0, fall_acceleration)
        r.Ragnarok.get_world().CollisionMgr.add_object(self.bounding_box)

    def set_default_pos(self, defaultPos):
        """Set the default starting location of our character."""
        self.coords = defaultPos
        self.velocity = r.Vector2()
        self.desired_position = defaultPos
        r.Ragnarok.get_world().Camera.pan = self.coords
        r.Ragnarok.get_world().Camera.desired_pan = self.coords

    def __step(self, old_pos, desired_pos):
        self.coords = desired_pos
        collisions = r.TileMapManager.active_map.grab_collisions(r.Vector2(old_pos.X, self.coords.Y))
        check_horizontal = True
        for collision in collisions:
            if "Solid" in collision.binding_type:
                self.coords.Y = old_pos.Y
                self.velocity.Y = 0

                #Reset the player state if the player isn't hitting a solid tile from down under.
                if collision.coords.Y > self.coords.Y:
                    self.CURRENT_STATE = self.NORMAL_STATE
            elif "Hazard" in collision.binding_type:
                self.hazard_touched_method(self)
                check_horizontal = False
                collisions = []
                break
            elif "Warp" in collision.binding_type:
                #Move the player to the new start location and start the next level.
                self.game_screen.level_manager.load_next_level()
                self.set_default_pos(r.TileMapManager.active_map.start_location)
                check_horizontal = False
                break
            elif "Reload" in collision.binding_type:
                self.set_default_pos(r.TileMapManager.active_map.start_location)
                check_horizontal = False

        if check_horizontal:
            collisions = r.TileMapManager.active_map.grab_collisions(r.Vector2(self.coords.X, old_pos.Y))
            for collision in collisions:
                if "Solid" in collision.binding_type:
                    self.coords.X = old_pos.X
                    self.velocity.X = 0
                elif "Hazard" in collision.binding_type:
                    self.hazard_touched_method(self)
                    collisions = []
                    break
                elif "Reload" in collision.binding_type:
                    self.set_default_pos(r.TileMapManager.active_map.start_location)
                    break

        self.desired_position = self.coords

    def __update_movement(self):
        old_pos = self.coords.copy()
        previous_position = self.coords.copy()
        direction = self.desired_position - old_pos
        y_step_count = int(abs(direction.Y) / 16) + 1
        x_step_count = int(abs(direction.X) / 16) + 1

        #This code prevents the block from ever moving more than one block per update cycle.
        if y_step_count > 1:
            old_pos = self.tile_map.pixels_to_tiles(old_pos)
            old_pos = self.tile_map.tiles_to_pixels(old_pos)
            self.desired_position.Y = old_pos.Y + (16 * r.sign(direction.Y))

        if x_step_count > 1:
            old_pos = self.tile_map.pixels_to_tiles(old_pos)
            old_pos = self.tile_map.tiles_to_pixels(old_pos)
            self.desired_position.X = old_pos.X + (16 * r.sign(direction.X))

        self.__step(old_pos, self.desired_position)

    def __handle_input(self, milliseconds):
        if r.Ragnarok.get_world().Keyboard.is_down(pygame.K_RIGHT):
            self.desired_position += r.Vector2(self.run_speed * (milliseconds / 1000.0), 0)
        if r.Ragnarok.get_world().Keyboard.is_down(pygame.K_LEFT):
            self.desired_position -= r.Vector2(self.run_speed * (milliseconds / 1000.0), 0)
        if r.Ragnarok.get_world().Keyboard.is_down(pygame.K_UP):
            if self.CURRENT_STATE != self.JUMPING_STATE:
                self.velocity = r.Vector2(0, -self.jump_velocity)
                self.CURRENT_STATE = self.JUMPING_STATE

    def update(self, milliseconds):
        if not self.is_paused:
            self.velocity += self.acceleration * (milliseconds / 1000.0)
            self.desired_position += self.velocity * (milliseconds / 1000.0)
            self.__update_movement()
            self.__handle_input(milliseconds)
            self.bounding_box.x = self.coords.X
            self.bounding_box.y = self.coords.Y
            r.Ragnarok.get_world().Camera.desired_pan = self.coords
            super(TileHeroCharacter, self).update(milliseconds)

    def draw(self, milliseconds, surface):
        if self.is_visible:
            surface.blit(self.image, self.coords)
