from Class import *
from Variables import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Object:
    def __init__(self, width, height, x0, y0, scale):
        # x0 and y0 refers to the left bottom point  position
        self.width = width
        self.height = height
        self.left = x0
        self.bottom = y0
        self.right = x0 + (scale * (width))
        self.top = y0 + (scale * (height))


def DrawRectangle(rect):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor(1,1,1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex(rect.left, rect.bottom, 0)
    glTexCoord2f(1, 0)
    glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1, 1)
    glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0, 1)
    glVertex(rect.left, rect.top, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)





def draw_text(string, x, y, scale, color):
    glMatrixMode(GL_MODELVIEW)
    glLineWidth(2)
    glColor(color[0], color[1], color[2])  # Yellow Color
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(scale, scale, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glLoadIdentity()
    glDisable(GL_TEXTURE_2D)


background = Object(1280, 720, 0, 0, 1)
splash_logo = Object(600, 300, WINDOW_WIDTH / 2 -
                     300, WINDOW_HEIGHT / 2, 1)
splash_tank = Object(171 / 2, 136 / 2, 100, 0, 1)
play = Object(600, 140, 500, 100, .5)
Gui_Panel = Object(1280, 150, 0, 0, 1)
Fire_Button = Object(185, 48, 546, 50, 1)
move_button = Object(185, 48, 304, 50, 1)
Angle_button = Object(185, 48, 1070, 50, 1)
power_slider = Object(185, 48, 808, 50, 1)
Weapon_Button = Object(173, 54, 0.3 * WINDOW_WIDTH, 0.01302 * WINDOW_HEIGHT, 1)
Weapon_type = Object(21, 21, (0.3 * WINDOW_WIDTH) + 10,
                     (0.01302 * WINDOW_HEIGHT) + 7, 1)
background_rec = Object(180, 720, 0, 0, 1)
#background = Object(1280, 720, 0, 0, 1)

############ Game_mode2_Gui ############
game_mode2_bg = Object(1280, 720, 0, 0, 1)
##Buttons##
Startgame_button = Object(336, 150, 180, 177, 1)
Resumegame_button = Object(336, 150, 180, 20, 1)

Audio_button = Object(85, 85, 842, 360, 1)
Music_button = Object(85, 85, 1072, 360, 1)
Settings_button = Object(85, 85, 958, 360, 1)
HTP_button = Object(162, 72, 920, 250, 1)
HE_MODES_button = Object(152, 68, 1006, 122, 1)
Theme_button = Object(152, 68, 842, 122, 1)
Easy_text = Object(71, 27, 1047, 138, 1)
Hard_text = Object(71, 22, 1047, 138, 1)
day_text = Object(61, 29, 888, 138, 1)
night_text = Object(87, 30, 871, 138, 1)
player_1_day = Object(161, 46, 13.8, 651, 1)
player_2_day = Object(168, 47, 1102, 651, 1)
player_1_night = Object(161, 46, 13.8, 651, 1)
player_2_night = Object(168, 47, 1102, 651, 1)
Exit_button = Object(128, 58, 710, 388, 1)
Newgame_button = Object(128, 58, 452, 388, 1)


##### sub windows####

subwindow_credits = Object(1280, 720, 0 , 0, 1)
Game_End_subwindows = Object(479, 192, 406, 369, 1)

####Night_buttons####
FireNight_button = Object(102, 102, 832, 20, 1)
moveNight_button = Object(111, 42, 622, 50, 1)
angle_power_button = Object(106, 106, 1011, 20, 1)

