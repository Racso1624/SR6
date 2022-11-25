#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR6

from gl import Render
from texture import *
from math import *
from vector import *

r = Render()

r.glCreateWindow(1024, 1024)

r.glClearColor(0.5, 0.6, 0.8)

r.glColor(0, 0, 0)

r.glClear()

textura = Texture('./human.bmp')

r.lookAt(V3(0, 0, 10), V3(0, 0, 0), V3(0, 1, 0))

r.loadModel('./human.obj', translate=[512, 512, 0], scale=[400, 400, 400], rotate=(0, 0, -pi/2), texture=textura)

r.glFinish("sr6.bmp")