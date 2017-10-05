# SkyGen
<img src="http://skygen.herokuapp.com/static/lang-logo.png" width="25%" height="25%"/><br>
It is good.<br>
SkyGen is a map generator I wrote in Python
You can see how It functions <a href="http://skygen.herokuapp.com">here</a>
The server for webapp is free so I strongly recommend these parameters:
Biome type: random
Rivers number: 20
Structures number: 20
Chunks number: 4
Minimal refactor height: 20
Maximal refactor height: 255
It should work just fine with them, other may cause an application error
(nothing bad will happen, but you won't get your map)
# Terrain
Terrain elevation generation works using fractal noise composed of OpenSimplex noisemaps
OpenSimplex noise is alternate version of Perlin's Simplex Noise algorithm with
no patent rights on it.
# Rivers
Rivers are generated simply by choosing random point above certain elevation and then chosing
one of adjacent ones with lowest elevation, and so on until we get to water or exceed river length limit.
# Structures
For now they're hardcoded but I will add procedurally generated ones in the future.
# Names
Using simple Markov's chain - based algorithm and text file with approximately 10000 fantasy city names as a seed
I procedurally generate random names for structures
# Clouds
Same as terrain but do not appear above certain elevation
# Rendering
For rendering I chose PyGame, so you'll need that if you want to try SkyGen on your computer
