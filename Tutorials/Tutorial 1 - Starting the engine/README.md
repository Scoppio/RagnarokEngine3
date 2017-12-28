Tutorial 1 - Getting Started
---

Based on the post from the original author, found on the Web Archive

## The Basics

The Ragnarok Engine is a simple and easy tool to create objects with animation and other complex behaviour without
having to deal too much reinventing the wheel

Here you will see how to import the engine and start a clean world.
The first step is to import our Ragnarok engine for use. If you installed it you simply have to do

```
    import Ragnarok as R
```

If instead you have the engine in your root directory of your project then you use

```
    from . import Ragnarok as R
```

## Initializing

Now to initialize the engine we must run one single line, which tells our system what is the size of the window we
are going to play the game, and what is the name of it.

```
    engine = R.Ragnarok(R.Vector2(640, 480), "RAGNAROK TUTORIAL 1")
```

We are telling Ragnarok that we want to create a window of size 640 by 480,
and that it should bear the title “RAGNAROK TUTORIAL 1″.
Notice how we are making use of the Vector2 class to pass in the window size.

One of Ragnarok’s goals is to reduce micro management in your code. It does this by automatically
updating and drawing your objects for you. You can control the draw and update order by changing an
object’s update_order and draw_order properties.
A low number will draw/update first, while a higher number will draw/update overtop the lower numbers.
Its like a z-index.

## World entity

The world is the entity within the engine that does all this work for us. We grab an instance of it here for easier access.

```
    world = engine.get_world()
```

The world’s clear_color property defines what color the backbuffer should be
erased to after each draw operation.

```
    world.clear_color = (255, 255, 255)
```

## Game loop

That’s it! All we have to do now is tell Ragnarok to begin spinning its game loop.

```
    engine.run()
```

At this point you should be presented with a blank white screen.
Don’t worry though, Ragnarok can do much more than this!

---

Check back in for Tutorial 2 to see how to add sprites and other entities to the world.