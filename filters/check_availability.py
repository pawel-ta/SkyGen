

def check_availability(lower_bound: int, upper_bound: int, high_lower_bound: int, map_array: list,
                       coordinates: tuple, size: int, scale_factor: int):
    """
    Function checks if there is enough space on map to generate structure of given size
        at given coordinates

    Args:
        lower_bound (int): elevation level above which structure can be generated
        upper_bound (int): elevation level below which structure can be generated
        high_lower_bound (int): elevation level above which structure can be generated
            despite the upper bound
        map_array (`obj`:list: of `obj`:list: of `obj`:int:): a list representing the map
        coordinates (`obj`:tuple: of `obj`:int:): a tuple with coordinates of central point
            of the structure
        size (int): size of the structure meaning the size in every direction from central point
        scale_factor (int): scale factor between structure pixel size and map pixel size, see
            generator.generate_sites()
    Returns
        Bool value indicating if there's enough free space for structure
    """

    if int((coordinates[0] + size)/scale_factor) >= len(map_array) or (coordinates[0] - size) < 0 or \
       int((coordinates[1] + size)/scale_factor) >= len(map_array[0]) or (coordinates[1] - size) < 0:
        return False

    for xk in range(-size, size):
        for yk in range(-size, size):
            if not (upper_bound >= map_array[int((coordinates[0] + xk) / scale_factor)]
                        [int((coordinates[1] + yk) / scale_factor)] > lower_bound or
                        map_array[int((coordinates[0] + xk) / scale_factor)]
                        [int((coordinates[1] + yk) / scale_factor)] > high_lower_bound):
                return False

    return True
