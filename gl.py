#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR6

import struct
from obj import *
from vector import *
from texture import *
import numpy as np
from math import *

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(h):
    #2 bytes
    return struct.pack('=h', h)

def dword(l):
    #4 bytes
    return struct.pack('=l', l)

def setColor(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

def bounding_box(A, B, C):

    coords = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

    x_min = 999999
    x_max = -999999
    y_min = 999999
    y_max = -999999

    for(x, y) in coords:

        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y

    return V3(x_min, y_min), V3(x_max, y_max)

def cross(v1, v2):
    return (
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )

def barycentric(A, B, C, P):

    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    if cz == 0:
        return(-1, -1, -1)

    u = cx / cz
    v = cy / cz
    w = 1 - (u + v)

    return(w, v, u)
        


class Render(object):

    def __init__(self):
        self.width = 0
        self.height = 0
        self.clear_color = setColor(1, 1, 1)
        self.render_color = setColor(0, 0, 0)
        self.viewport_color = setColor(1, 1, 1)
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_height = 0
        self.viewport_width = 0
        self.texture = None
        self.light = V3(0, 0, 1)
        self.Model = None
        self.View = None
        self.Projection = None

    def glClear(self):
        self.framebuffer = [[self.clear_color for x in range(self.width)]
        for y in range(self.height)]

        self.zBuffer = [
            [-999999 for x in range(self.width)]
            for y in range(self.height)
        ]

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewportColor(self, r, g, b):
        self.viewport_color = setColor(r, g, b)

    def glClearColor(self, r, g, b):
        self.clear_color = setColor(r, g, b)

    def glClearViewport(self):
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                self.glPoint(x,y, self.viewport_color)    
        

    def glColor(self, r, g, b):
        self.render_color = setColor(r, g, b)

    def glViewPort(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def glVertex(self, x, y):
        if x > 1 or x < -1 or y > 1 or y < -1:
            print('Error')
        else:
            x = int((x + 1) * (self.viewport_width / 2) + self.viewport_x)
            y = int((y + 1) * (self.viewport_height / 2) + self.viewport_y)

            self.glPoint(x, y)

    def glPoint(self, x, y, color = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.framebuffer[x][y] = color or self.render_color

    def glLine(self, x0, x1, y0, y1, color = None):
        
        line_color = color or self.render_color

        x0 = round(x0)
        x1 = round(x1)
        y0 = round(y0)
        y1 = round(y1)

        if x0 == x1:
            if y0 == y1:
                self.glPoint(x0, y0, line_color)
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0

        threshold = dx

        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(x, y, line_color)
            else:
                self.glPoint(y, x, line_color)

            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2

    def transform_vertex(self, vertex):
        augmented_vertex = [
            vertex[0],
            vertex[1],
            vertex[2],
            1
        ]

        transformed_vertex = self.Projection @ self.View @ self.Model @ augmented_vertex
        transformed_vertex = V3(transformed_vertex)

        return V3(
            transformed_vertex.x / transformed_vertex.w,
            transformed_vertex.y / transformed_vertex.w,
            transformed_vertex.z / transformed_vertex.w
        )

    def loadModel(self, filename, translate, scale, rotate, texture = None):
        
        self.loadModelMatrix(translate, scale, rotate)
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face)
            
            if vcount == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex(model.vertices[f1])
                v2 = self.transform_vertex(model.vertices[f2])
                v3 = self.transform_vertex(model.vertices[f3])
                v4 = self.transform_vertex(model.vertices[f4])

                if not texture:
                    self.triangle(v1, v2, v3)
                    self.triangle(v1, v3, v4)
                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1
                    t4 = face[3][1] - 1

                    tA = V3(*model.tvertices[t1])
                    tB = V3(*model.tvertices[t2])
                    tC = V3(*model.tvertices[t3])
                    tD = V3(*model.tvertices[t4])

                    self.triangle(v1, v2, v3, (tA, tB, tC), texture)
                    self.triangle(v1, v3, v4, (tA, tC, tD), texture)

            
            elif vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex(model.vertices[f1])
                v2 = self.transform_vertex(model.vertices[f2])
                v3 = self.transform_vertex(model.vertices[f3])

                if not texture:
                    self.triangle(v1, v2, v3)
                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1

                    tA = V3(*model.tvertices[t1])
                    tB = V3(*model.tvertices[t2])
                    tC = V3(*model.tvertices[t3])

                    self.triangle(v1, v2, v3, (tA, tB, tC), texture)

    def loadModelMatrix(self, translate, scale, rotate):

        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translation_matrix = np.matrix([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
        ])

        scale_matrix = np.matrix([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ])

        rotation_x = np.matrix([
            [1,             0,              0, 0],
            [0, cos(rotate.x), -sin(rotate.x), 0],
            [0, sin(rotate.x),  cos(rotate.x), 0],
            [0,             0,              0, 1]
        ])

        rotation_y = np.matrix([
            [ cos(rotate.y), 0, sin(rotate.y), 0],
            [             0, 1,             0, 0],
            [-sin(rotate.y), 0, cos(rotate.y), 0],
            [             0, 0,             0, 1]
        ])

        rotation_z = np.matrix([
            [cos(rotate.z), -sin(rotate.z), 0, 0],
            [sin(rotate.z),  cos(rotate.z), 0, 0],
            [            0,              0, 1, 0],
            [            0,              0, 0, 1]
        ])

        rotation_matrix = rotation_x @ rotation_y @ rotation_z

        self.Model = translation_matrix @ rotation_matrix @ scale_matrix

    def loadViewMatrix(self, x, y, z, center):
        Mi = matrix([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [  0,   0,   0, 1],
        ])

        Op = matrix([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ])

        self.View = Mi @ Op

    
    def loadProjectionMatrix(self, eye, center):
        coeff = -1 / (eye.length() - center.length())

        self.Projection = matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ])

    def lookAt(self, eye, center, up):
        z = (eye - center).norm()
        x = (up * z).norm()
        y = (z * x).norm()

        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(eye, center)


    def triangle(self, A, B, C, cord_tex = None, texture = None, color = None, intensity = 1):
    
        normal = (B - A) * (C - A)
        i = normal.norm() @ self.light.norm()

        if i < 0:
            i = abs(i)
        if i > 1:
            i = 1

        color_tex = 1 * i

        self.render_color = setColor(color_tex, color_tex, color_tex)

        min, max = bounding_box(A, B, C)
        min.round_coords()
        max.round_coords()
        
        for x in range(min.x, max.x):
            for y in range(min.y, max.y):
                w, v, u = barycentric(A, B, C, V3(x, y))

                if(w < 0 or v < 0 or u < 0):
                    continue
                
                if texture:
                    tA, tB, tC = cord_tex
                    tx = tA.x * w + tB.x * u + tC.x * v
                    ty = tA.y * w + tB.y * u + tC.y * v

                    color = texture.get_color_with_intensity(tx, ty, intensity)

                z = A.z * w + B.z * v + C.z * u
                if(x < len(self.zBuffer) and y < len(self.zBuffer[0]) and z > self.zBuffer[x][y]):
                    self.zBuffer[x][y] = z
                    self.glPoint(x, y, color)


    def glFinish(self, filename):
        f = open(filename, 'bw')

        #pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range (self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()