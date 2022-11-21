#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR5

from gl import Render
from texture import *

r = Render()

r.glCreateWindow(1024, 1024)

r.glClearColor(0.5, 0.6, 0.8)

r.glColor(0, 0, 0)

r.glClear()

textura = Texture('./earth.bmp')

r.load('./earth.obj', translate=[512, 512, 0], scale=[1, 1, 1], texture=textura)

r.glFinish("sr5.bmp")