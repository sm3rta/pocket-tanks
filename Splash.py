from tex_load import *
from Gui import *
from Class import *
import winsound
from Variables import *


def rect1():

    glColor(Color('00b9ff'))
    glColor(Color('ffffff'))

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(0, 70, 0)
    glTexCoord2f(1, 1)
    glVertex3f(300, 70, 0)
    glTexCoord2f(1, 0)
    glVertex3f(300, 0, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def mouse_motion(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = WINDOW_HEIGHT - y


def Logo_display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    background_tex.draw_tex()
    background.build_center()

    glLoadIdentity()
    pocket_tanks_intro_tex.draw_tex()
    pocket_tanks.build_center()

alpha = 0
xt = 0
R = 1
L = 0


def splash_display():
    global xt, yt, R, L, c, r_angle, newmouse_x, newmouse_y, alpha

    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    init_tex(splash_background_tex, background, alpha)

    if alpha <= 1:
        alpha += 0.002

    glLoadIdentity()

    if (play.left <= mouse_x <= play.right and play.bottom <= mouse_y <= play.top):
        init_tex(play_button_b, play, alpha)
    else:
        init_tex(play_button_r, play, alpha)

    glDisable(GL_TEXTURE_2D)
    glLoadIdentity()
    init_tex(splash_logo_tex, splash_logo, alpha)

    glLoadIdentity()
    if R:
        init_tex(splash_tank_r_tex, splash_tank, alpha, xt)
    if L:
        init_tex(splash_tank_l_tex, splash_tank, alpha, xt)

    glLoadIdentity()
    glColor(0, 1, 0)
    glutSolidSphere(50, 30, 30)

    glutSwapBuffers()

    c = -c
    r_angle += 0.8

    if xt > 1000 - 150 or L:
        R = 0
        L = 1
        xt -= 0.8
    if xt < 100 or R:
        R = 1
        L = 0
        xt += 0.8
