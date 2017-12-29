Tutorial 2 - Adding Sprites
---

Based on the post from the original author, found on the Web Archive

## The Sprite

It is extremely simple to add objects to the world in Ragnarok.
All you have to do is create the object and call add_obj from the Ragnarok engine instance.
Below follows a more in-depth example:

A Sprite is essentially a container object for an image that allows us to manipulate properties of it extremely easily.
Let’s start by creating the object.

```
    sprite = RE3.Sprite()
```

## The Properties

Since we are adding only one object to the world, the update and draw orders don’t carry much significance as of yet.
But if we were to add more than one object, these values would be responsible for controlling the order in which the
object updates and draws in relation to other objects.

```
    sprite.update_order = 0
    sprite.draw_order = 0
```

## Load texture

Now we assign an image to the sprite by going to the Ragnarok Engine folder and pulling out its logo image.

```
    sprite.load_texture("Ragnarok.jpg")
```

## The World Entity (again)

Now, remember in the previous tutorial how we said that the World is the entity responsible for
managing our objects for us? Well, the last step to get this object onscreen is to
add it to the world so it can be drawn and updated.

```
    world.add_obj(sprite)
```

Boom! That’s all it takes to get an sprite on the screen.
You can play around with the sprite’s *coords*, *scale*, and *rotation* properties to change the orientation of the
sprite accordingly.

## The coordinate system

The coordinate system is a little different from most, it makes the screen a simple 4 quadrants coordinate system,
with the origin (x=0,y=0) in the middle, the top is minus half the height (-H/2) and the bottom is half the height(H/2),
the left side is minus half the width of the window screen (-W/2) and the right is the half width of the window
screen (W/2)

## Run it

```
    engine.run()
```