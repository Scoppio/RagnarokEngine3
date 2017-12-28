import Ragnarok as r
import pygame
import os

font_path = os.path.join("..", "Fonts")
font_path = os.path.join(font_path, "foo.ttf")

class WinScreen(r.DrawableObj):
    def __init__(self):
        super(WinScreen, self).__init__(self)
        self.winText = r.Text(0, 0, font_path, 84, (255, 255, 255))
        self.winText.text = "You Won!"
        self.winText.coords = r.Vector2(800 / 2.0, 600 / 2.0)
        self.is_enabled = False
        self.is_visible = False

    def show(self):
        self.is_enabled = True
        self.is_visible = True

    def draw(self, milliseconds, surface):
        pygame.draw.rect(surface, (0,0,0,175), pygame.Rect(0, 0, 800, 600))
        self.winText.draw(milliseconds, surface)

class LoseScreen(r.DrawableObj):
    def __init__(self, char):
        global lose_creation_count
        super(LoseScreen, self).__init__(self)
        self.winText = r.Text(0, 0, font_path, 84, (255, 255, 255))
        self.winText.text = "You Lost!"
        self.winText.coords = r.Vector2(800 / 2.0, 600 / 2.0)
        self.spaceText = r.Text(0, 0, font_path, 32, (255, 255, 255))
        self.spaceText.text = "Hit Space"
        self.spaceText.coords = self.winText.coords + r.Vector2(0, 128)
        self.is_enabled = False
        self.is_visible = False
        self.char = char
        self.delay_timer = r.Timer(500)

    def show(self):
        self.delay_timer.is_enabled = True
        self.char.is_paused = True

    def update(self, milliseconds):
        if self.delay_timer.is_enabled:
            self.delay_timer.update(milliseconds)
            if self.delay_timer.is_ringing():
                self.is_enabled = True
                self.is_visible = True
                self.delay_timer.is_enabled = False
                self.delay_timer.reset()

        if self.is_enabled:
            if r.Ragnarok.get_world().Keyboard.is_clicked(pygame.K_SPACE):
                #Restart the level.
                self.char.CURRENT_STATE = self.char.NORMAL_STATE
                self.char.set_default_pos(r.TileMapManager.active_map.start_location)
                self.is_enabled = False
                self.is_visible = False
                self.char.is_paused = False
                r.Ragnarok.get_world().remove_obj(self)

    def draw(self, milliseconds, surface):
        if self.is_visible:
            pygame.draw.rect(surface, (0,0,0,175), pygame.Rect(0, 0, 800, 600))
            self.winText.draw(milliseconds, surface)
            self.spaceText.draw(milliseconds, surface)