from tex_load import *


""" From Rgb to hex.
#changing the Lazer Colors
"""


def hex_color(Color):
    a = Color[0] // 16
    b = Color[0] % 16
    c = Color[1] // 16
    d = Color[1] % 16
    e = Color[2] // 16
    f = Color[2] % 16

    L = []
    for i in [a, b, c, d, e, f]:
        if i == 10:
            i = 'A'
        if i == 11:
            i = 'B'
        if i == 12:
            i = 'C'
        if i == 13:
            i = 'D'
        if i == 14:
            i = 'E'
        if i == 15:
            i = 'F'
        L.append(str(i))

    return "".join(L)


""" From hex to RGB.
"""


def Color(hex_string):
    if len(hex_string) == 6:
        a = int(hex_string[:2], 16)
        b = int(hex_string[2:4], 16)
        c = int(hex_string[4:], 16)
        return (a / 256, b / 256, c / 256)


""" Rectangle used in tanks and turret.
"""


class Rectangle:
    def __init__(self, width, height, pos, angle, color):
        self.width = width
        self.height = height
        self.x = pos[0]
        self.y = pos[1]
        self.angle = angle
        self.color = color


    """ Build rectangles from it's center.
    # tanks
    """

    def build_center(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(self.x, self.y, 0)
        glRotate(self.angle, 0, 0, 1)
        glColor(Color(self.color))
        glBegin(GL_POLYGON)

        glTexCoord2f(0, 0)
        glVertex(-self.width / 2, -self.height / 2)
        glTexCoord2f(0, 1)
        glVertex(-self.width / 2, self.height / 2)
        glTexCoord2f(1, 1)
        glVertex(self.width / 2, self.height / 2)
        glTexCoord2f(1, 0)
        glVertex(self.width / 2, -self.height / 2)
        glEnd()
        glDisable(GL_TEXTURE_2D)
    """ Build rectangles from it's center.
    # tanks
    """

    def build_corner(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(self.x, self.y, 0)
        glRotate(self.angle, 0, 0, 1)
        glColor(Color(self.color))
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex(0, 0)
        glTexCoord2f(0, 1)
        glVertex(0, self.height)
        glTexCoord2f(1, 1)
        glVertex(self.width, self.height)
        glTexCoord2f(1, 0)
        glVertex(self.width, 0)
        glEnd()

""" Build rectangles from it's center.
# tanks
"""


class Tank(Rectangle):
    def __init__(self, name, score, pos, tank_angle, turret_angle, color, power, moves, weapons):
        self.name = name
        self.score = score
        self.pos = pos
        self.tank_angle = tank_angle
        self.turret_angle = turret_angle
        self.color = color
        self.power = power
        self.moves = moves
        self.weapons = weapons
        self.selected_weapon = 0

    def build(self):
        glEnable(GL_TEXTURE_2D)
        x = Rectangle(171 * 0.3/1.3, 136 * 0.3/1.3,
                      self.pos, self.tank_angle, self.color)  # 171 * 0.3, 136 * 0.3
        x.build_center()
        glDisable(GL_TEXTURE_2D)
        turret_tex.draw_tex()
        y = Rectangle(73 / 3, 18 / 3, self.pos,
                      self.turret_angle, "FFFFFF")
        y.build_corner()
