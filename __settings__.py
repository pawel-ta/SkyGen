class MAP_RESOLUTION:
    x = 30
    y = 30

OCTAVES = 4
OCTAVE_WAVELENGTH = [100, 20, 5, 1]
OCTAVE_AMPLITUDE = [127, 10, 5, 1]
MAP_PIXEL_SIZE = 5
SITE_PIXEL_SIZE = 2
WATER_LEVEL_STEP = 5
NUMBER_OF_CHUNKS = 5

class LEVELS:
    water = 80
    beach = 90
    grass = 140
    dirt = 160
    stone = 210
    snow = 255

class BIOME_COLOR:
    class rgb_color:
        def __init__(self, r: int, g: int, b: int):
            self._r = r
            self._g = g
            self._b = b

        @property
        def r(self):
            return self._r

        @property
        def g(self):
            return self._g

        @property
        def b(self):
            return self._b

    water = {
        'default' : rgb_color(23, 107, 181),
        'tropical' : rgb_color(85, 227, 232),
        'north' : rgb_color(225, 244, 240)
    }
    beach = {
        'default' : rgb_color(221, 210, 157),
        'tropical' : rgb_color(255, 233, 183),
        'north' : rgb_color(169, 173, 172)
    }
    grass = {
        'default' : rgb_color(39, 181, 63),
        'tropical' : rgb_color(149, 193, 73),
        'north' : rgb_color(96, 140, 115)
    }
    dirt = {
        'default' : rgb_color(99, 79, 56),
        'tropical' : rgb_color(186, 107, 27),
        'north' : rgb_color(82, 91, 63)
    }
    stone = {
        'default' : rgb_color(119, 115, 111),
        'tropical' : rgb_color(204, 114, 74),
        'north' : rgb_color(150, 150, 158),
    }
    snow = {
        'default' : rgb_color(237, 237, 237),
        'tropical' : rgb_color(214, 64, 0),
        'north' : rgb_color(244, 255, 254)
    }
    wood = {
        'default' : rgb_color(104, 53, 35),
        'tropical': rgb_color(104, 53, 35),
        'north': rgb_color(104, 53, 35)
    }
    stone_brick = {
        'default': rgb_color(49, 45, 41),
        'tropical': rgb_color(44, 44, 44),
        'north': rgb_color(40, 40, 48),
    }