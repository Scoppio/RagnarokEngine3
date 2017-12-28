import Ragnarok as R
import pygame
import random
import os

# Init our engine.
engine = R.Ragnarok(R.Vector2(800, 600), "RAGNAROK TUTORIAL 3")
world = engine.get_world()
world.clear_color = (0, 0, 0)


# In this tutorial we will demostrate how to create custom components and add them to the world.
# There are many options we have here. The most common course of action is to inherit
# from Ragnarok's Sprite, Animation, UpdatableObject, or DrawableObj types.
# Inherit from UpdatableObj only if the object should update and not draw. If the object is to display
# on the screen, than update from a type that can draw onscreen.
# It is good design practice to inherit from DrawableObject if the class is to display more than one sprite.
# The sun, for example, is made up of the sun texture and a rotating sun ray texture, thus it makes
# more sense to inherit from DrawableObj than it is to inherit from anything else.
class Sun(R.DrawableObj):
    def __init__(self, draw_order, update_order):
        """
        Creates a sun with rotating sun rays that follows the mouse around the screen.
        """
        # Super calls the init method of the base class, allowing the
        # component to be seen as a sprite object by Ragnarok.
        super(Sun, self).__init__(draw_order, update_order)

        # Keep in mind that the object we are creating is custom, so we can
        # do anything we want to with it. Since this object is the sun, we will
        # give it a few behaviours. First of all, it should have Sun Rays that rotate around
        # the sun. The sun, should also follow the mouse around the screen.
        # Let's start by initing up our sun sprite. (See tutorial 2 for info on this process.)

        # We use os.path.join here to ensure the path to our texture will work on
        # multiple operating systems.
        sun_path = os.path.join("Textures", "Sun.png")
        self.sun = R.Sprite()
        self.sun.load_texture(sun_path)

        # Get backbuffer size gets the size of the screen. We divide by 2 to get the center, and then set
        # the sun's coords to the result, placing the sun at the center of the window as its default position.
        self.sun.coords = R.Ragnarok.get_world().get_backbuffer_size() / 2.0
        self.sun.scale = (.35, .35)

        # Let's now create another sprite inside our custom component that represents
        # the Sun Rays around the sun.
        sun_rays_path = os.path.join("Textures", "SunRays.png")
        self.sun_rays = R.Sprite()
        self.sun_rays.load_texture(sun_rays_path)
        self.sun_rays.coords = self.coords
        self.sun_rays.scale = (.95, .95)

        # rotation_val is the amount our sun rays have currently rotated.
        self.rotation_val = 0.0

    # Defining an update method that accepts milliseconds as a parameter
    # (milliseconds is the amount of time that elapsed betten the current and last frame) allows
    # Ragnarok to automatically call this method every update.
    def update(self, milliseconds):
        # Get the location of the mouse.
        mouse_pos = pygame.mouse.get_pos()

        # Set the location of the sun and its rays to the current mouse location.
        self.sun.coords.X = mouse_pos[0]
        self.sun.coords.Y = mouse_pos[1]
        self.sun_rays.coords.X = mouse_pos[0]
        self.sun_rays.coords.Y = mouse_pos[1]

        # Rotate the sun rays at 10 degrees per second.
        # Dividing milliseconds by 1000 effectively converts milliseconds into seconds.
        self.rotation_val += 10 * (milliseconds / 1000.0)
        self.sun_rays.rotation = self.rotation_val

        self.sun.update(milliseconds)
        self.sun_rays.update(milliseconds)

        # (Optional) Call the update method of the base class (DrawableObj).
        super(Sun, self).update(milliseconds)

    # Defining the draw method here is the same as defining the update method above,
    # it allows us to define component specific behavior.
    # Note that if we don't redefine these than the standard Ragnarok.DrawableObj draw and update methods
    # will be called.
    def draw(self, milliseconds, surface):
        # All we have to do now is call the draw methods of the
        # sun and sun_rays sprites to get them to draw on the screen.
        self.sun.draw(milliseconds, surface)
        self.sun_rays.draw(milliseconds, surface)

        # (Optional) Call the draw method of the base class (DrawableObj).
        super(Sun, self).draw(milliseconds, surface)


# Since this class doesn't contain any more than one object it makes
# good design practice to inherit directly from Sprite.
class Cloud(R.Sprite):
    """
    Creates a cloud that slowly wafts across the sky.
    """

    def __init__(self, draw_order, update_order):
        super(Cloud, self).__init__(draw_order, update_order)
        cloud_path = os.path.join("Textures", "Cloud.png")
        self.load_texture(cloud_path)

        # Pick a random location on the screen where the cloud will appear.
        x_rand = random.randrange(0, 800)
        y_rand = random.randrange(0, 100)
        self.coords = R.Vector2(x_rand, y_rand)

        # Pick a random size that the cloud should be.
        scale_val = random.randrange(1, 3)
        self.scale = (scale_val, scale_val)

        # Pick a random movement speed for the cloud. This determines how fast our
        # cloud will move across the screen. The speed is in pixels per second.
        self.movement_speed = random.randrange(10, 35)

    def __generate_location(self):
        """
        Reset the location of the cloud once it has left the viewable area of the screen.
        """
        screen_width = world.get_backbuffer_size().X
        self.movement_speed = random.randrange(10, 25)

        # This line of code places the cloud to the right of the viewable screen, so it appears to
        # gradually move in from the right instead of randomally appearing on some portion of the viewable
        # window.
        self.coords = R.Vector2(screen_width + self.image.get_width(), random.randrange(0, 100))

    def update(self, milliseconds):
        # Update the movement of the cloud by moving it horizontally across the screen.
        # Dividing milliseconds by 1000 effictively converts milliseconds into seconds.
        # This allows us to easily move the clouds in pixels per second.
        move_amt = self.movement_speed * (milliseconds / 1000.0)
        self.coords = R.Vector2(self.coords.X - move_amt, self.coords.Y)

        # Check to see if the cloud has moved off the visible area of the screen.
        if self.coords.X < (-self.image.get_width() * 3):
            # Reset the location of the cloud
            self.__generate_location()

        # Call the update method of the base class (Sprite).
        super(Cloud, self).update(milliseconds)

    # Notice that we don't override the draw method here.
    # We don't do this because we don't have any Cloud-specific draw
    # code that needs executed.


# Here is an example of an object that inherits from UpdatableObj.
# All this object does is exit the game when Escape is pressed.
# It doesn't have to draw onto the screen whatsoever.
class ExitManager(R.UpdatableObj):
    """
    In this case, allows the Esc button to exit the game.
    """

    def update(self, milliseconds):
        if R.Ragnarok.get_world().Keyboard.is_clicked(pygame.K_ESCAPE):
            engine.exit()


# Create our sky and ground sprites.
sky_path = os.path.join("Textures", "sky.png")
sky = R.Sprite()
sky.load_texture(sky_path)
sky.scale_to(world.get_backbuffer_size())

ground_path = os.path.join("Textures", "grass.png")
ground = R.Sprite(4, 4)
ground.load_texture(ground_path)
ground.scale_to(world.get_backbuffer_size())
ground.coords.Y = world.get_backbuffer_size().Y * .75

sun = Sun(1, 1)
exit_manager = ExitManager()

# Create an array of clouds to move across the screen.
clouds = []
for cloud in range(2):
    clouds.append(Cloud(3, 3))

# Add all of our objects to the world.
world.add_obj(sky)
world.add_obj(ground)
world.add_obj(sun)
world.add_obj(exit_manager)

# Add each cloud to the world.
for cloud in clouds:
    world.add_obj(cloud)

# Run our game.
engine.run()
