import struct

def setColor(r, g, b):
    return bytes([int(b), int(g), int(r)])

class Texture(object):

    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        with open(self.path, "rb") as image:
            image.seek(10)
            header_size = struct.unpack("=l", image.read(4))[0]
            image.seek(18)
            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]
            image.seek(header_size)

            self.pixels = []
            for y in range(self.height):
                self.pixels.append([])

                for x in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    
                    self.pixels[y].append(
                        setColor(r, g, b)
                    )

    def get_color(self, tx, ty):
        x = round(tx * self.width)
        y = round(ty * self.height)

        return self.pixels[y][x]

    def get_color_with_intensity(self, tx, ty, intensity):
        x = round(tx * self.width)
        y = round(ty * self.height)

        try:
            return bytes(map(lambda b: round(b*intensity) 
                if b*intensity > 0 
                else 0, 
                self.pixels[y][x])
            )
        except:
            pass