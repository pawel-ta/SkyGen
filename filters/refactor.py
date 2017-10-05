from __settings__ import *
from opensimplex import OpenSimplex
from random import randint
from filters.int_median_cutter import int_median_cutter

def refactor(map_array: list, min_height: int, max_height: int):
    """
    Function blending map composed from rectangular chunks into seamless one, without visible borders

    Args:
        map_array (`obj`:list: of `obj`:list: of `obj`:int:): a list representing the map
        min_height (int): integer indicating minimal height after refactoring
        max_height (int): integer indicating maximal height after refactoring
    Returns:
        map_array (`obj`:list: of `obj`:list: of `obj`:int:): a list representing the map,
            but now with smooth borders between chunks!
    """

    smoothness = 1

    if min_height < 0:
        min_height = 1
    if max_height > 255:
        max_height = 255

    for _ in range(50):
        for x in range(smoothness, len(map_array) - smoothness):
            for y in range(smoothness, len(map_array[0]) - smoothness):
                map_array[x][y] = int((map_array[x - smoothness][y - smoothness] +
                                       map_array[x - smoothness][y + smoothness] +
                                       map_array[x + smoothness][y - smoothness] +
                                       map_array[x + smoothness][y + smoothness]) / 4)

    noise_maker = OpenSimplex(randint(-10000, 10000))

    for x in range(len(map_array)):
        for y in range(len(map_array[0])):
            for octave in range(OCTAVES):
                if map_array[x][y] > LEVELS.water or octave < 1:
                    map_array[x][y] = int_median_cutter(min_height,
                                                        max_height,
                                                        map_array[x][y] + 2 *
                                                        OCTAVE_AMPLITUDE[octave] *
                                                        noise_maker.noise2d((x) / OCTAVE_WAVELENGTH[octave],
                                                                            (y) / OCTAVE_WAVELENGTH[octave]))

            map_array[x][y] = int_median_cutter(0, 255, map_array[x][y] + 2 * OCTAVE_AMPLITUDE[3] *
                                          noise_maker.noise2d(x / OCTAVE_WAVELENGTH[3],
                                                              y / OCTAVE_WAVELENGTH[3]))
            map_array[x][y] = int_median_cutter(0, 255, map_array[x][y] + 2 * OCTAVE_AMPLITUDE[3] *
                                          noise_maker.noise2d(x / OCTAVE_WAVELENGTH[2],
                                                              y / OCTAVE_WAVELENGTH[2]))

    return map_array
