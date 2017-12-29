from setuptools import setup, find_packages

description = """
Ragnarok Engine was first started in 2010 by Clinton Myers, it is small and concise 2D game engine built on top 
of Pygame to make game creation easier.

While Pygame is a library, Ragnarok attempts to assume the role of an engine, featuring many capabilities that would
take a lot of work to create from the ground up in Pygame.

The engine is built in such a way that it attempts to be used under any scenario and game environment.
It is easy to set up, maintain, and extend for your particular needs.
This code is being expanded and ported to python 3.6

## Features

Many basic classes and methods are already inplace for Ragnarok Engine3
- 2D and 3D Vector Math Library
- Sprites with easy rotation, scaling, texture loading, etc.
- SpriteSheet and Animation classes
- Text objects that can be rotated, scaled, and translated
- A customizable 2D Camera
- A managed World system that updates, draws, and automatically offsets objects by the camera's translation.
- Collision System
- Input Handling Systems
- Particle Systems
- Pool class for efficiently reusing objects
- TileMaps

## How to install

To install, download the distribution, unpackage it and inside the folder you run.

    pip install .

## How to use

You should look the tutorials for more information at the github of the project,
To verify if it is working properly you may simply create a minimum project.

      import Ragnarok as R

      engine = R.Ragnarok(R.Vector2(640, 480), "RAGNAROK WHITE SCREEN")

      world = engine.get_world()
      world.clear_color = (255, 255, 255)

      engine.run()
"""

setup(
      name='RagnarokEngine3',
      version='1.0.0a9',
      description='Simple and easy 2D game engine for pygame applications',
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: pygame',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
      ],
      keywords='pygame python3 engine game',
      author='Lucas Scoppio',
      author_email='lucascoppio@gmail.com',
      url='https://github.com/Scoppio/Ragnarok-Engine3',
      license='LGPL 3',
      packages=['RagnarokEngine3'],
      long_description=description,
      zip_safe=True,
      install_requires=[
          'pygame==1.9.3',
      ],
      python_requires='>=3.6.*, <4',
      )
