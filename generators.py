from random import randint
from numpy.random import randint as numint
from opensimplex import OpenSimplex
from filters.int_median_cutter import int_median_cutter
from filters.check_availability import check_availability
from __settings__ import *


def generate_map_chunk(size_x: int, size_y: int, biome_type: str, x_offset: int = 0, y_offset: int = 0):
    """
    Function responsible for generating map chunk in specified or random biome type,
        map chunk is basically a rectangular part of a map;
        generated array is basically nested list representing a 2d-array, where
        fields are integers indicating elevation of certain point.
        For generating map chunk I use OpenSimplex noise generator, which is
        a deterministic coherent (gradient) noise generator, The chunk is randomised
        by chosing random seed for the generator object initialisation.

    Args:
        size_x (int): horizontal size of chunk in map pixels
        size_y (int): vertical size of chunk in map pixels
        biome_type (str): string indicating which biome type to use
        x_offset (int): integer indicating horizontal offset used in generating Simplex Noise
        y_offset (int): integer indicating vertical offset used in generating Simplex Noise
    Returns:
        map_array (:obj:`list` of :obj:`list` of :obj:`int`): list of lists containing elevation
            number for specified coordinates
    """
    map_array = []
    for _ in range(size_x):
        map_array_part = []
        for _ in range(size_y):
            map_array_part.append(127)
        map_array.append(map_array_part)

    noise_maker = OpenSimplex(randint(-10000, 10000))

    for x in range(size_x):
        for y in range(size_y):
            for octave in range(OCTAVES):
                if map_array[x][y] > LEVELS.water or octave < 1:
                    map_array[x][y] = int_median_cutter(0, 255,
                                      map_array[x][y]+OCTAVE_AMPLITUDE[octave]*\
                                      noise_maker.noise2d((x+x_offset)/OCTAVE_WAVELENGTH[octave],
                                      (y+y_offset)/OCTAVE_WAVELENGTH[octave]))

    if biome_type == 'random':
        biome_type = ['ocean_islands',
                      'ocean',
                      'high_mountains',
                      'default'][randint(0,3)]

    if biome_type == 'ocean_islands':
        for x in range(size_x):
            for y in range(size_y):
                map_array[x][y] = max(map_array[x][y] - 100, 20)
    elif biome_type == 'ocean':
        for x in range(size_x):
            for y in range(size_y):
                map_array[x][y] = max(int(map_array[x][y]*0.3125), 20)
    elif biome_type == 'high_mountains':
        for x in range(size_x):
            for y in range(size_y):
                map_array[x][y] = min(map_array[x][y] + 100 + 10 *
                                      noise_maker.noise2d(x/OCTAVE_WAVELENGTH[1],
                                      y/OCTAVE_WAVELENGTH[1]), 250)
    return map_array


def generate_map(chunks_number: int, map_res_x: int, map_res_y: int):
    """
    Function responsible for generating a list representing map, each point
        has an integer value meaning it's elevation (from 0 to 255)
    
    Args:
        chunks_number (int): number of chunks (vertical and horizontal is the same)
        map_res_x (int): horizontal size of single chunk
        map_res_y (int): vertical size of single chunk
    Returns:
        map_array (:obj:`list` of :obj:`list` of :obj:`int`): list of lists containing elevation
                number for specified coordinates
    """
    biome_list = []
    for _ in range(pow(chunks_number, 2)):
        biome_list.append(generate_map_chunk(map_res_x, map_res_y, 'random'))

    map_array = []
    for x in range(int(pow(len(biome_list), 0.5)) * map_res_x):
        map_array.append([])
        for y in range(int(pow(len(biome_list), 0.5)) * map_res_y):
            map_array[x].append(biome_list[int((x) / map_res_x) + int(pow(len(biome_list), 0.5)) *
                                           int((y) / map_res_y)][x % int(map_res_x)][
                                    y % int(map_res_y)])
    return map_array


def create_namespace(map_array: list):
    """
    Function generating a list indicating where on the map names can be generated
        initialised with 0's, used in generate_sites where 0's are changed to 1's
        in place of generated sites

    Args:
        map_array (:obj:`list` of :obj:`list` of :obj:`int`): list
            representing map with elevation
    Returns:
        namespace (:obj:`list` of :obj:`list` of :obj:`int`): list
            in the size of map_array initialised with 0's
    """
    namespace = []
    for x in range(len(map_array)*MAP_PIXEL_SIZE):
        namespace.append([])
        for _ in range(len(map_array[0])*MAP_PIXEL_SIZE):
            namespace[x].append(0)
    return namespace


def generate_sites(map_array: list, map_namespace: list, quantity: int = 0):
    """
    Function responsible for generating a list representing various structures on map,
        for now they're all hardcoded, I will introduce procedurally generated sites
        in future versions of SkyGen

    Args:
        map_array (:obj:`list` of :obj:`list` of :obj:`int`): a list representing the map
        map_namespace (:obj:`list` of :obj:`list` of :obj:`int`): a list initialised with
        0's in the size of map_array
        quantity (int): amount of structures to be generated
    Returns:
        sites_array (:obj:`list` of :obj:`list` of :obj:`int`): a list
            representing sites on map
    """
    sites_array = []
    scale_factor = MAP_PIXEL_SIZE/SITE_PIXEL_SIZE
    sites_factor_x = int(scale_factor * len(map_array))
    sites_factor_y = int(scale_factor * len(map_array[0]))

    if scale_factor < 1:
        scale_factor = 1

    for x in range(sites_factor_x):
        sites_array.append([])
        for y in range(sites_factor_y):
            sites_array[x].append(0)

    if quantity == -1:
        number_of_sites = randint(10,20)
    else:
        number_of_sites = quantity

    site_types = [2, 2, 2, 3, 5, 11, 15, 21, 'ship']

    max_number_of_fortresses = randint(1, 2)
    max_number_of_grand_cities = 1
    max_number_of_villages = 2
    max_number_of_ships = 5

    rx = numint(25, len(sites_array) - 25, size=20000)
    ry = numint(25, len(sites_array[0]) - 25, size=20000)

    while number_of_sites > 0:

        x = rx[len(rx)-1]
        y = ry[len(ry)-1]

        rx = rx[:-1]
        ry = ry[:-1]

        site_type = site_types[randint(0,len(site_types)-1)]

        if site_type != 'ship':
            for xk in range(-int(3*site_type/2), int(3*site_type/2)):
                for yk in range(-int(3*site_type/2), int(3*site_type/2)):
                    if x+xk < 0 or x+xk > (len(sites_array) - 1):
                        break
                    if y+yk < 0 or y+yk > (len(sites_array[0]) - 1):
                        break
                    if sites_array[x+xk][y+yk] != 0:
                        site_type = 0

        if site_type == 2:
            if check_availability(LEVELS.water, LEVELS.grass, 256, map_array, (x,y), site_type, scale_factor):
                sites_array[x][y] = 1
                sites_array[x][y+1] = 1
                sites_array[x+1][y+1] = 1
                sites_array[x+1][y] = 1
        elif site_type == 3:
            if check_availability(LEVELS.water, LEVELS.grass, 256, map_array, (x,y), site_type, scale_factor):
                sites_array[x][y] = 2
                sites_array[x+1][y] = 1
                sites_array[x-1][y] = 1
                sites_array[x][y+1] = 1
                sites_array[x][y-1] = 1
                number_of_sites -= 1
        elif site_type == 5:
            if check_availability(LEVELS.water, LEVELS.grass, 256, map_array, (x,y), site_type, scale_factor):
                sites_array[x][y] = 1
                sites_array[x+1][y] = 1
                sites_array[x-1][y] = 1
                sites_array[x][y+1] = 1
                sites_array[x][y-1] = 1
                sites_array[x+1][y+1] = 2
                sites_array[x-1][y+1] = 2
                sites_array[x-1][y-1] = 2
                sites_array[x+1][y-1] = 2
                sites_array[x][y-2] = 1
                sites_array[x][y+2] = 1
                sites_array[x+2][y] = 1
                sites_array[x-2][y] = 1
                number_of_sites -= 1
                map_namespace[x*SITE_PIXEL_SIZE][y*SITE_PIXEL_SIZE] = 5
        elif site_type == 11 and max_number_of_villages:
            if check_availability(LEVELS.water, LEVELS.grass, LEVELS.stone, map_array, (x, y), site_type, scale_factor):
                for _ in range(50):
                    sites_array[x + randint(-11, 11)][y + randint(-11, 11)] = 1
                sites_array[x][y] = 2
                sites_array[x + 1][y] = 2
                sites_array[x - 1][y] = 2
                sites_array[x][y + 1] = 2
                sites_array[x][y - 1] = 2
                sites_array[x + 1][y + 1] = 2
                sites_array[x - 1][y + 1] = 2
                sites_array[x - 1][y - 1] = 2
                sites_array[x + 1][y - 1] = 2
                number_of_sites -= 1
                map_namespace[x * SITE_PIXEL_SIZE][y * SITE_PIXEL_SIZE] = 11
                max_number_of_villages -= 1
        elif site_type == 15 and max_number_of_fortresses != 0:
            if check_availability(LEVELS.water, LEVELS.grass, LEVELS.stone, map_array, (x, y), site_type, scale_factor):
                for _ in range(60):
                    sites_array[x + randint(-15, 15)][y + randint(-15, 15)] = 1
                sites_array[x][y] = 1
                sites_array[x + 1][y] = 1
                sites_array[x - 1][y] = 1
                sites_array[x][y + 1] = 1
                sites_array[x][y - 1] = 1
                sites_array[x + 1][y + 1] = 1
                sites_array[x - 1][y + 1] = 1
                sites_array[x - 1][y - 1] = 1
                sites_array[x + 1][y - 1] = 1
                sites_array[x + 2][y] = 1
                sites_array[x - 2][y] = 1
                sites_array[x][y + 2] = 1
                sites_array[x][y - 2] = 1
                sites_array[x + 2][y + 2] = 1
                sites_array[x - 2][y + 2] = 1
                sites_array[x - 2][y - 2] = 1
                sites_array[x + 2][y - 2] = 1

                rand_prob_1 = randint(4,5)
                rand_prob_2 = randint(4,5)

                towers = [randint(0, 1), randint(0, 1), randint(0, 1), randint(0, 1)]

                for k in range(-15, -3):
                    if not randint(0, 10) % rand_prob_1:
                        sites_array[x + k][y - 15] = 1
                        sites_array[x + k][y + 15] = 1
                        sites_array[x - 15][y + k] = 1
                        sites_array[x + 15][y + k] = 1
                        sites_array[x + k][y - 13] = 1
                        sites_array[x + k][y + 13] = 1
                        sites_array[x - 13][y + k] = 1
                        sites_array[x + 13][y + k] = 1
                for k in range(3, 15):
                    if not randint(0, 10) % rand_prob_2:
                        sites_array[x + k][y - 15] = 1
                        sites_array[x + k][y + 15] = 1
                        sites_array[x - 15][y + k] = 1
                        sites_array[x + 15][y + k] = 1
                        sites_array[x + k][y - 13] = 1
                        sites_array[x + k][y + 13] = 1
                        sites_array[x - 13][y + k] = 1
                        sites_array[x + 13][y + k] = 1
                if towers[0]:
                    sites_array[x + 15][y + 15] = 2
                    sites_array[x + 14][y + 15] = 2
                    sites_array[x + 15][y + 14] = 2
                    sites_array[x + 14][y + 14] = 2
                    sites_array[x + 15][y + 13] = 2
                    sites_array[x + 14][y + 13] = 2
                    sites_array[x + 13][y + 14] = 2
                    sites_array[x + 13][y + 15] = 2
                    sites_array[x + 13][y + 13] = 2
                elif towers[1]:
                    sites_array[x - 15][y + 15] = 2
                    sites_array[x - 14][y + 15] = 2
                    sites_array[x - 15][y + 14] = 2
                    sites_array[x - 14][y + 14] = 2
                    sites_array[x - 15][y + 13] = 2
                    sites_array[x - 14][y + 13] = 2
                    sites_array[x - 13][y + 14] = 2
                    sites_array[x - 13][y + 15] = 2
                    sites_array[x - 13][y + 13] = 2
                elif towers[2]:
                    sites_array[x - 15][y - 15] = 2
                    sites_array[x - 14][y - 15] = 2
                    sites_array[x - 15][y - 14] = 2
                    sites_array[x - 14][y - 14] = 2
                    sites_array[x - 15][y - 13] = 2
                    sites_array[x - 14][y - 13] = 2
                    sites_array[x - 13][y - 14] = 2
                    sites_array[x - 13][y - 15] = 2
                    sites_array[x - 13][y - 13] = 2
                elif towers[3]:
                    sites_array[x + 15][y - 15] = 2
                    sites_array[x + 14][y - 15] = 2
                    sites_array[x + 15][y - 14] = 2
                    sites_array[x + 14][y - 14] = 2
                    sites_array[x + 15][y - 13] = 2
                    sites_array[x + 14][y - 13] = 2
                    sites_array[x + 13][y - 14] = 2
                    sites_array[x + 13][y - 15] = 2
                    sites_array[x + 13][y - 13] = 2
                number_of_sites -= 1
                max_number_of_fortresses -= 1
                map_namespace[x * SITE_PIXEL_SIZE][y * SITE_PIXEL_SIZE] = 15
        elif site_type == 21 and max_number_of_grand_cities != 0:
            if check_availability(LEVELS.water, LEVELS.grass, LEVELS.stone, map_array, (x, y), site_type, scale_factor):
                for xk in range(-21, 21):
                    for yk in range(-21, 21):
                        if randint(0, int(pow(xk*xk+yk*yk, 0.5))) < 3 and (xk*xk+yk*yk) <= 21*21:
                            if (xk*xk+yk*yk) < 16:
                                sites_array[x + xk][y + yk] = 2
                            else:
                                sites_array[x + xk][y + yk] = 1
                            number_of_sites -= 1
                            max_number_of_grand_cities -= 1
                            map_namespace[
                                x * SITE_PIXEL_SIZE][
                                y * SITE_PIXEL_SIZE] = 21
        elif site_type == 'ship' and max_number_of_ships:
            if check_availability(0, LEVELS.water, 256, map_array, (x, y), 5, scale_factor):
                ship_direction = randint(1,4)
                if ship_direction == 1:
                    sites_array[x][y] = 2
                    sites_array[x][y+1] = 2
                    sites_array[x][y-1] = 1
                    sites_array[x+1][y] = 1
                    sites_array[x-1][y] = 1
                    sites_array[x-1][y-1] = 1
                    sites_array[x+1][y-1] = 1
                    sites_array[x][y+2] = 1
                    sites_array[x-1][y+2] = 1
                    sites_array[x+1][y+2] = 1
                    sites_array[x-1][y+1] = 1
                    sites_array[x+1][y+1] = 1
                    sites_array[x][y+3] = 1
                elif ship_direction == 2:
                    sites_array[x][y] = 2
                    sites_array[x][y-1] = 2
                    sites_array[x][y+1] = 1
                    sites_array[x+1][y] = 1
                    sites_array[x-1][y] = 1
                    sites_array[x-1][y+1] = 1
                    sites_array[x+1][y+1] = 1
                    sites_array[x][y-2] = 1
                    sites_array[x-1][y-2] = 1
                    sites_array[x+1][y-2] = 1
                    sites_array[x-1][y-1] = 1
                    sites_array[x+1][y-1] = 1
                    sites_array[x][y-3] = 1
                elif ship_direction == 3:
                    sites_array[x][y] = 2
                    sites_array[x+1][y] = 2
                    sites_array[x-1][y] = 1
                    sites_array[x][y+1] = 1
                    sites_array[x][y-1] = 1
                    sites_array[x-1][y-1] = 1
                    sites_array[x-1][y+1] = 1
                    sites_array[x+2][y] = 1
                    sites_array[x+2][y-1] = 1
                    sites_array[x+2][y+1] = 1
                    sites_array[x+1][y-1] = 1
                    sites_array[x+1][y+1] = 1
                    sites_array[x+3][y] = 1
                elif ship_direction == 4:
                    sites_array[x][y] = 2
                    sites_array[x-1][y] = 2
                    sites_array[x+1][y] = 1
                    sites_array[x][y+1] = 1
                    sites_array[x][y-1] = 1
                    sites_array[x+1][y-1] = 1
                    sites_array[x+1][y+1] = 1
                    sites_array[x-2][y] = 1
                    sites_array[x-2][y-1] = 1
                    sites_array[x-2][y+1] = 1
                    sites_array[x-1][y-1] = 1
                    sites_array[x-1][y+1] = 1
                    sites_array[x-3][y] = 1
                number_of_sites -= 1
                max_number_of_ships -= 1

    return sites_array


def generate_rivers(map_array: list, map_res_x: int, map_res_y: int, quantity: int = 0):
    """
    Function generating rivers on map array by decreasing terrain elevation, algorithm
        looks for random point above certain elevation (LEVELS.dirt) and then makes it
        under water level, next point is chosen as the point from neighbouring points
        with the lowest elevation

    Args:
        map_array (:obj:`list` of :obj:`list` of :obj:`int`): a list representing the map
        map_res_x (int): resolution of a single chunk (horizontal)
        map_res_y (int): resolution of a single chunk (vertical)
        quantity (int): number of rivers to be generated on map
    Returns:
        map_array (:obj:`list` of :obj:`list` of :obj:`int`): a list representing the map,
            same as that given as input but with rivers on it!
    """
    while quantity != 0:

        x = randint(0, len(map_array) - 1)
        y = randint(0, len(map_array[0]) - 1)

        if map_array[x][y] > LEVELS.dirt:
            next_point = [x, y]
            safe_counter = max(map_res_x, map_res_y)*NUMBER_OF_CHUNKS

            while not map_array[next_point[0]][next_point[1]] < LEVELS.water and safe_counter > 0:
                map_array[next_point[0]][next_point[1]] = LEVELS.water - randint(0, WATER_LEVEL_STEP*4)
                kill_while = False
                minimal = 999
                for xk in [-1, 0, 1]:
                    for yk in [-1, 0, 1]:
                        old_minimal = minimal
                        if not (0 < (next_point[0] + xk) < (len(map_array) - 1) and
                                0 < (next_point[1] + yk) < (len(map_array[0]) - 1)):
                            kill_while = True
                            break
                        if min(map_array[next_point[0] + xk][next_point[1] + yk], minimal) > LEVELS.water and \
                                                abs(xk)+abs(yk) != 2:
                            minimal = min(map_array[next_point[0] + xk][next_point[1] + yk], minimal)
                        if minimal < old_minimal:
                            next_point = [next_point[0]+xk, next_point[1]+yk]
                    if kill_while:
                        break
                if kill_while:
                    break
                safe_counter -= 1
            quantity -= 1
    return map_array


def generate_clouds(map_array: list, elevation: int):
    """
    Function responsible for generating clouds on certain elevation

    Args:
        map_array (:obj:`list` of :obj:`list` of :obj:`int`): a list representing the map
        elevation (int): the elevation of clouds layer
    Returns:
        cloud_array map_array (:obj:`list` of :obj:`list` of :obj:`int`): a list representing clouds
    """
    cloud_array = []

    noise_maker_clouds = OpenSimplex(randint(10000, 100000))

    for x in range(len(map_array)):
        cloud_array.append([])
        for y in range(len(map_array[0])):
            if map_array[x][y] < elevation:
                cloud_array[x].append(int_median_cutter(0, 210,
                                          OCTAVE_AMPLITUDE[0]*\
                                          noise_maker_clouds.noise2d((x)/OCTAVE_WAVELENGTH[0],
                                          (y)/OCTAVE_WAVELENGTH[0])))
                for octave in range(1,3):
                    cloud_array[x][y] = int_median_cutter(0, 210,
                                          cloud_array[x][y] + OCTAVE_AMPLITUDE[octave]*\
                                          noise_maker_clouds.noise2d((x)/OCTAVE_WAVELENGTH[octave],
                                          (y)/OCTAVE_WAVELENGTH[octave]))
            else:
                cloud_array[x].append(0)

    return cloud_array
