#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR6

from gl import Render
from texture import *
from math import *

r = Render()

r.glCreateWindow(1024, 1024)

r.glClearColor(0.5, 0.6, 0.8)

r.glColor(0, 0, 0)

r.glClear()

textura = Texture('./cup_tex.bmp')

r.loadModel('./cup.obj', translate=[300, 800, 0], scale=[50, 50, 50], rotate=(0, pi/3, -pi/2), texture=textura)

r.glFinish("sr6.bmp")