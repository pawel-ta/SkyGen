from display import display_on_surface
from filters.refactor import refactor
from generators import generate_map, generate_sites, generate_rivers, create_namespace
from __settings__ import *

map_array = generate_map(NUMBER_OF_CHUNKS, MAP_RESOLUTION.x, MAP_RESOLUTION.y)

refactor(map_array, 20, 255)

map_namespace = create_namespace(map_array)

sites_array = generate_sites(map_array, map_namespace, 30)

generate_rivers(map_array, MAP_RESOLUTION.x, MAP_RESOLUTION.y, 20)

display_on_surface(map_array, sites_array, map_namespace, 'random', True, True)