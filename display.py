import pygame
from random import randint, seed, random
from opensimplex import OpenSimplex
from __settings__ import *
from name_generator.name_generator import generate_random_name
from generators import generate_clouds

def display_on_surface(map_array: list, sites_array: list, map_namespace: list,
                       biome: str, display_names: bool, display_clouds: bool):
    """
    Functions that displays map ARTISTICALLY on the pygame's surface
        (pygame display on desktop, surface in the webapp), display is shittycoded,
        but it's for purpose of easily creating nice looks
    Args:
        map_array (`obj`:list: of `obj`:list: of `obj`:int:): a list representing the map
        sites_array (`obj`:list: of `obj`:list: of `obj`:int:): a list representing sites
        map_namespace (`obj`:list: of `obj`:list: of `obj`:int:): a list representing
            where names on map should be placed, they're generated during display_on_surface
            by name_generator.generate_random_name
        biome (str): string containing the name of the biome, you can see available names in __settings__.py,
            when 'random' is entered as it chooses random biome type
        display_names (bool): whether the names should be generated and displayed on the map
        display_clouds (bool): whether clouds should be generated and displayed on the map
    Returns:
        map_name (str): for Django Web Application generates random number for the name of
            the file in which map is to be saved
    """

    pygame.init()

    window = pygame.display.set_mode((len(map_array)*MAP_PIXEL_SIZE, len(map_array[0])*MAP_PIXEL_SIZE))

    pygame.display.set_caption("Talaga's SkyGen 2017")

    pygame.display.set_icon(pygame.image.load("static/lang-logo.png"))

    noise_maker = OpenSimplex(randint(-10000, 10000))

    if biome == 'random':
        biome = ['default', 'tropical', 'north'][randint(0, 2)]

    if biome == 'north':
        water_depth = 0.3
    elif biome == 'tropical':
        water_depth = 0.6
    else:
        water_depth = 1

    for x in range(len(map_array)):
        for y in range(len(map_array[0])):
            if map_array[x][y] <= LEVELS.water:
                color = pygame.Color(BIOME_COLOR.water[biome].r - int(water_depth*BIOME_COLOR.water[biome].r*abs(LEVELS.water-map_array[x][y])/LEVELS.water/WATER_LEVEL_STEP)*WATER_LEVEL_STEP,
                                     BIOME_COLOR.water[biome].g - int(water_depth*BIOME_COLOR.water[biome].g*abs(LEVELS.water-map_array[x][y])/LEVELS.water/WATER_LEVEL_STEP)*WATER_LEVEL_STEP,
                                     BIOME_COLOR.water[biome].b - int(water_depth*BIOME_COLOR.water[biome].b*abs(LEVELS.water-map_array[x][y])/LEVELS.water/WATER_LEVEL_STEP)*WATER_LEVEL_STEP, 0)
            elif map_array[x][y] <= LEVELS.beach:
                color = pygame.Color(min(max(BIOME_COLOR.beach[biome].r + randint(-15, 15), 0), 252),
                                     min(max(BIOME_COLOR.beach[biome].g + randint(-15, 15), 0), 252),
                                     min(max(BIOME_COLOR.beach[biome].b + randint(-15, 15), 0), 252), 0)
            elif map_array[x][y] <= LEVELS.grass:
                color = pygame.Color(min(BIOME_COLOR.grass[biome].r - abs(int((BIOME_COLOR.grass[biome].r - 19)*noise_maker.noise2d(x/OCTAVE_WAVELENGTH[0], 0.5*y/OCTAVE_WAVELENGTH[0])))
                                     + randint(0, 40), 256),
                                     max(min(BIOME_COLOR.grass[biome].g - abs(int((BIOME_COLOR.grass[biome].g - 81)*noise_maker.noise2d(x/OCTAVE_WAVELENGTH[0], 0.5*y/OCTAVE_WAVELENGTH[0])))
                                     + randint(-20, 20), 256), 0),
                                     max(min(BIOME_COLOR.grass[biome].b - abs(int((BIOME_COLOR.grass[biome].r - 43)*noise_maker.noise2d(x/OCTAVE_WAVELENGTH[0], 0.5*y/OCTAVE_WAVELENGTH[0])))
                                     + randint(-43, 25), 256), 0), 0)
            elif map_array[x][y] <= LEVELS.dirt:
                seed(int(x*y/pow(OCTAVE_WAVELENGTH[2], 2)))
                if (2*random() - 1) > 0.5:
                    color = pygame.Color(BIOME_COLOR.dirt[biome].r ,
                                         BIOME_COLOR.dirt[biome].g,
                                         BIOME_COLOR.dirt[biome].b, 0)
                elif (2*random() - 1) > 0.3:
                    color = pygame.Color(max(BIOME_COLOR.dirt[biome].r - 9, 0),
                                         max(BIOME_COLOR.dirt[biome].g - 9, 0),
                                         max(BIOME_COLOR.dirt[biome].b - 9, 0), 0)
                elif (2*random() - 1) > 0.1:
                    color = pygame.Color(max(BIOME_COLOR.dirt[biome].r - 19, 0),
                                         max(BIOME_COLOR.dirt[biome].g - 19, 0),
                                         max(BIOME_COLOR.dirt[biome].b - 19, 0), 0)
                elif (2*random() - 1) > -0.2:
                    color = pygame.Color(max(BIOME_COLOR.dirt[biome].r - 29, 0),
                                         max(BIOME_COLOR.dirt[biome].g - 19, 0),
                                         max(BIOME_COLOR.dirt[biome].b - 19, 0), 0)
                elif (2*random() - 1) > -0.5:
                    color = pygame.Color(max(BIOME_COLOR.dirt[biome].r - 29, 0),
                                         max(BIOME_COLOR.dirt[biome].g - 29, 0),
                                         max(BIOME_COLOR.dirt[biome].b + 1, 0), 0)
                else:
                    color = pygame.Color(max(BIOME_COLOR.dirt[biome].r - 39, 0),
                                         max(BIOME_COLOR.dirt[biome].g - 35, 0),
                                         max(BIOME_COLOR.dirt[biome].b - 12, 0), 0)
            elif(map_array[x][y] <= LEVELS.stone):
                color = pygame.Color(min(max(BIOME_COLOR.stone[biome].r - abs(int(10\
                                    *int(5*noise_maker.noise2d(x/OCTAVE_WAVELENGTH[1], 0.5*y/OCTAVE_WAVELENGTH[1])))), 0), 256),
                                     min(max(BIOME_COLOR.stone[biome].g - abs(int(10\
                                    *int(5*noise_maker.noise2d(x/OCTAVE_WAVELENGTH[1], 0.5*y/OCTAVE_WAVELENGTH[1])))), 0), 256),
                                    min(max(BIOME_COLOR.stone[biome].b - abs(int(10\
                                    *int(5*noise_maker.noise2d(x/OCTAVE_WAVELENGTH[1], 0.5*y/OCTAVE_WAVELENGTH[1])))), 0), 256),
                                     0)
            else:
                color = pygame.Color(min(max(BIOME_COLOR.snow[biome].r + randint(-15, 15), 0), 255),
                                     min(max(BIOME_COLOR.snow[biome].g + randint(-15, 15), 0), 255),
                                     min(max(BIOME_COLOR.snow[biome].b + randint(-15, 15), 0), 255), 0)

            tmp_rect = pygame.Rect((x*MAP_PIXEL_SIZE,y*MAP_PIXEL_SIZE), (MAP_PIXEL_SIZE, MAP_PIXEL_SIZE))
            pygame.draw.rect(window, color, tmp_rect)

    for x in range(len(sites_array)):
        for y in range(len(sites_array[0])):
            if sites_array[x][y] != 0:
                if sites_array[x][y] == 1:
                    color = pygame.Color(BIOME_COLOR.wood[biome].r, BIOME_COLOR.wood[biome].g, BIOME_COLOR.wood[biome].b, 0)
                if sites_array[x][y] == 2:
                    color = pygame.Color(BIOME_COLOR.stone_brick[biome].r, BIOME_COLOR.stone_brick[biome].g, BIOME_COLOR.stone_brick[biome].b, 0)
                tmp_rect = pygame.Rect((x * SITE_PIXEL_SIZE, y * SITE_PIXEL_SIZE), (SITE_PIXEL_SIZE, SITE_PIXEL_SIZE))
                pygame.draw.rect(window, color, tmp_rect)

    pygame.font.init()
    font_path = "static/lunchds.ttf"
    font_size = 14
    font_small = pygame.font.Font(font_path, font_size)
    font_med = pygame.font.Font(font_path, font_size+2)
    font_big = pygame.font.Font(font_path, font_size+4)

    if display_clouds:
        clouds_array = generate_clouds(map_array, LEVELS.stone)
        for x in range(len(clouds_array)):
            for y in range(len(clouds_array[0])):
                tmp_rect = pygame.Surface((MAP_PIXEL_SIZE, MAP_PIXEL_SIZE))
                tmp_rect.set_alpha(clouds_array[x][y])
                tmp_rect.fill((225, 225, 225, clouds_array[x][y]))
                window.blit(tmp_rect,(MAP_PIXEL_SIZE * x, MAP_PIXEL_SIZE * y))

    if display_names:
        for x in range(len(map_namespace)):
            for y in range(len(map_namespace[0])):
                if map_namespace[x][y] == 5:
                    site_name = font_small.render(generate_random_name('names_seed'), 1, (255, 255, 255), (0, 0, 0))
                    offset = int(site_name.get_width() / 2)
                    site_name.set_alpha(150)
                    window.blit(site_name, (x - offset, y))
                if map_namespace[x][y] == 11:
                    site_name = font_med.render(generate_random_name('names_seed'), 1, (255, 255, 255), (0, 0, 0))
                    offset = int(site_name.get_width() / 2)
                    site_name.set_alpha(150)
                    window.blit(site_name, (x - offset, y))
                if map_namespace[x][y] == 15:
                    site_name = font_big.render(generate_random_name('names_seed'), 1, (255, 255, 255), (0, 0, 0))
                    offset = int(site_name.get_width() / 2)
                    site_name.set_alpha(150)
                    window.blit(site_name, (x - offset, y))
                if map_namespace[x][y] == 21:
                    site_name = font_big.render(generate_random_name('names_seed'), 1, (255, 255, 255), (0, 0, 0))
                    offset = int(site_name.get_width() / 2)
                    site_name.set_alpha(150)
                    window.blit(site_name, (x - offset, y))

    map_name = str(randint(0,1000000))

    surface_tmp = pygame.Surface((window.get_width(), window.get_height()))

    surface_tmp.blit(window,(0, 0))

    rect_name = font_big.render("SAVE MAP", 1, (255, 255, 255), (0, 0, 0))

    window.blit(rect_name, (window.get_width() - rect_name.get_width() - 10, 10))

    frame_saved_count = 0

    rect_saved = font_big.render("SAVED", 1, (255, 255, 255), (0, 0, 0))


    while True:
        pygame.display.flip()
        event = pygame.event.wait()
        while frame_saved_count:
            rect_saved.set_alpha(frame_saved_count)
            window.blit(surface_tmp, (0, 0))
            window.blit(rect_saved, (window.get_width() - rect_saved.get_width() - 25, 10))
            pygame.display.flip()
            frame_saved_count -= 1
            if frame_saved_count == 0:
                window.blit(rect_name, (window.get_width() - rect_name.get_width() - 10, 10))
        if event.type == pygame.MOUSEBUTTONDOWN:
            position_mouse = pygame.mouse.get_pos()
            if position_mouse[0] > (window.get_width() - rect_name.get_width() - 10) and\
                position_mouse[0] < (window.get_width() + 10) and\
                position_mouse[1] < (rect_name.get_height() + 10) and\
                position_mouse[1] > (10):
                pygame.image.save(surface_tmp,'generated_maps/'+str(randint(0,100000000))+'_map.png')
                frame_saved_count = 255
        elif event.type == pygame.QUIT:
            break

    return map_name