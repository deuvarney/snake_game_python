from collections import namedtuple

Colour = namedtuple("Colour", ["red", "green", "blue"])
TEAL = Colour(red=36, green=188, blue=168)  # Teal
BLACK = Colour(red=0, green=0, blue=0) # Black
WHITE = Colour(red=255, green=255, blue=255)
GREEN = Colour(red=0, green=255, blue=0) # Green
RED = Colour(red=255, green=0, blue=0)
FOOD = Colour(red=23, green=78, blue=200) # ???
SNAKE_HEAD = Colour(red=60, green=200, blue=60) # Light Green
