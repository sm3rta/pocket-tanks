from Class import *
import numpy as np
from math import atan, sin, cos, radians
from random import randrange
from scipy.interpolate import interp1d
from Splash import *
from Variables import *

###############################################################################
################################ VARIABLES ####################################
###############################################################################

pocket_tanks = Rectangle(600, 300, [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 200], 0, "FFFFFF")
tank1 = Tank("Player 1", 0, [100, 0], 0, 0, "FFFFFF", 85, 6, [randrange(0, 7, 1) for _ in range(10)])
tank2 = Tank("Player 2", 0, [1000, 0], 0, 180, "FFFFFF", 85, 6, [randrange(0, 7, 1) for _ in range(10)])
active_tank = tank1
other_tank = tank2

# initialize weapons projectiles here:
single_shot_projectile = Rectangle(40, 40, (-5, -5), 0, "FFFFFF")  # single shot
bazooka_projectile = Rectangle(14, 3, (-5, -5), 0, "FFFFFF")  # bazooka
super_lazer_projectile = Rectangle(14, 3, (-5, -5), 0, "FFFFFF")  # super lazer
three_shot_projectile_1 = Rectangle(10, 11, (-5, -5), 0, "FFFFFF")  # 3 shot - 1
three_shot_projectile_2 = Rectangle(10, 11, (-5, -5), 0, "FFFFFF")  # 3 shot - 2
three_shot_projectile_3 = Rectangle(10, 11, (-5, -5), 0, "FFFFFF")  # 3 shot - 3
skipper_projectile = Rectangle(15, 16, (-5, -5), 0, "FFFFFF")
skipper_projectile_2 = Rectangle(15, 16, (-5, -5), 0, "FFFFFF")
skipper_projectile_3 = Rectangle(15, 16, (-5, -5), 0, "FFFFFF")
tommy_gun_projs = []
for i in range(8):  # tommy gun 8 projectiles
    tommy_gun_projs.append(Rectangle(10, 11, (-5, -5), 0, "EEEEEE"))
tommy_gun_projectile_1, tommy_gun_projectile_2, tommy_gun_projectile_3, tommy_gun_projectile_4, tommy_gun_projectile_5, tommy_gun_projectile_6 \
    , tommy_gun_projectile_7, tommy_gun_projectile_8 = tommy_gun_projs
tommy_gun_random_powers = [randrange(-4, 5, 1) for _ in range(8)]
tommy_gun_random_angles = [randrange(-4, 5, 1) for _ in range(8)]   
acid_rain_projectile = Rectangle(14, 14, (-5, -5), 0, "000000")
acid_rain_small_projectile_1 = Rectangle(2, 2, (-5, -5), 0, "000000")
acid_rain_small_projectile_2 = Rectangle(2, 2, (-5, -5), 0, "000000")
acid_rain_small_projectile_3 = Rectangle(2, 2, (-5, -5), 0, "000000")
acid_rain_small_projectile_4 = Rectangle(2, 2, (-5, -5), 0, "000000")
acid_rain_small_projectile_5 = Rectangle(2, 2, (-5, -5), 0, "000000")
# skipper_projectile = Rectangle(2, 2, (-5, -5), 0, "DDDD11")
skipper_c = 0


###############################################################################
############################# DRAWING ON SCREEN ###############################
###############################################################################

def draw_circle(x_start, x_end, r, x0=0, y0=0, x_3rd=1, y_3rd=1):
    glBegin(GL_LINE_STRIP)
    while x_start <= x_end:
        x1 = x_3rd * (x0 + r * cos(x_start))
        y1 = y_3rd * (y0 + r * sin(x_start))
        glVertex(x1, y1)
        x_start += 0.1
    glEnd()


def world_shape():
    x = np.linspace(0, WINDOW_WIDTH, num=16, endpoint=True)
    y = [randrange(200, hardness, 1) for i in range(len(x))]
    return interp1d(x, y, kind='cubic')


def init_world_shape():
    global f
    f = world_shape()


def draw_world():
    x = np.linspace(0, WINDOW_WIDTH, num=80, endpoint=True)

    if view_mode == 1:
        earth_day_tex.draw_tex()
    else:
        earth_night_tex.draw_tex()
    glBegin(GL_QUADS)
    glColor(1, 1, 1)
    for i in range(len(x) - 1):
        glTexCoord2f(0, 0)
        glVertex(x[i], 0)
        glTexCoord2f(1, 0)
        glVertex(x[i], f(x[i]))
        glTexCoord2f(1, 1)
        glVertex(x[i + 1], f(x[i + 1]))
        glTexCoord2f(0, 1)
        glVertex(x[i + 1], 0)
    glEnd()


def world_shape_param(x0, x1):
    y1 = f(x0)
    y2 = f(x1)
    return y1, y2


###############################################################################
################################ MOVEMENT #####################################
###############################################################################

def move_left():
    global active_tank
    if active_tank.moves > 0 and active_tank.pos[0] > 40:
        if active_tank == tank1:
            tank1.pos[0] -= 21
            calc_tank1_pos()
        elif active_tank == tank2:
            tank2.pos[0] += 19
            calc_tank2_pos()


def move_right():
    global active_tank
    if active_tank.moves > 0 and active_tank.pos[1] < WINDOW_WIDTH - 40:
        if active_tank == tank1:
            tank1.pos[0] -= 19
            calc_tank1_pos()
        elif active_tank == tank2:
            tank2.pos[0] += 21
            calc_tank2_pos()


def calc_tank1_pos():
    global tank1
    tank1_y = world_shape_param(tank1.pos[0] - 20, tank1.pos[0] + 20)
    m1 = (tank1_y[1] - tank1_y[0]) / 55
    tank1.tank_angle = atan(m1) * 57.2957795
    tank1.pos[1] = tank1_y[1] + 15
    tank1.pos[0] += 20


def calc_tank2_pos():
    global tank2
    tank2_y = world_shape_param(tank2.pos[0] + 20, tank2.pos[0] - 20)
    m2 = (tank2_y[0] - tank2_y[1]) / 55
    tank2.tank_angle = atan(m2) * 57.2957795
    tank2.pos[1] = tank2_y[1] + 15
    tank2.pos[0] -= 20


###############################################################################
############################# MOUSE ANS KEYBOARD ##############################
###############################################################################
if music == 1:
    winsound.PlaySound('Sounds/Burt Bacharach.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
def mouseonclick(button, state, x, y):
    global fire, mouse_On, mouse_x, mouse_y, Fire_Button, move_button, right, left, credits_sub_menu, active_tank, game_mode, newmouse_x, newmouse_y, Sounds, music, hardness, Theme, tank1, tank2, Resume, Game_End_subwindow, left_slider_out, right_slider_out, wepons_left_out, wepons_right_out
    if time == 0:
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            newmouse_x = x
            newmouse_y = WINDOW_HEIGHT - y
            if game_mode == 0:
                if (play.left <= newmouse_x <= play.right and play.bottom <= newmouse_y <= play.top):
                    game_mode = 1
                if Sounds == 1:
                    winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif game_mode == 1:
                if credits_sub_menu == 0:
                    
                    if Startgame_button.left <= newmouse_x <= Startgame_button.right and Startgame_button.bottom <= newmouse_y <= Startgame_button.top:
                        init_world_shape()
                        tank1.score = 0
                        tank2.score = 0
                        tank1.pos=[200, 0]
                        tank2.pos=[1080, 0]
                        active_tank = tank1
                        tank1.moves = 6
                        tank2.moves = 6
                        tank1.weapons, tank2.weapons = [randrange(0, 7, 1) for _ in range(10)], [randrange(0, 7, 1) for _ in range(10)]
                        calc_tank1_pos()
                        calc_tank2_pos()
                        projs_init()
                        Resume = 1
                        game_mode = 2

                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE| winsound.SND_ASYNC )
                    if Resumegame_button.left <= newmouse_x <= Resumegame_button.right and Resumegame_button.bottom <= newmouse_y <= Resumegame_button.top:
                        if Resume == 1:
                            game_mode = 2
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE | winsound.SND_ASYNC )
                    if Settings_button.left <= newmouse_x <= Settings_button.right and Settings_button.bottom <= newmouse_y <= Settings_button.top:
                        credits_sub_menu = 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE | winsound.SND_ASYNC )
                    if Audio_button.left <= newmouse_x <= Audio_button.right and Audio_button.bottom <= newmouse_y <= Audio_button.top:
                        if Sounds == 0:
                            Sounds = 1
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE | winsound.SND_ASYNC )
                        elif Sounds == 1:
                            Sounds = 0
                    if HE_MODES_button.left <= newmouse_x <= HE_MODES_button.right and HE_MODES_button.bottom <= newmouse_y <= HE_MODES_button.top:
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE | winsound.SND_ASYNC )
                        if hardness == 250:
                            hardness = 400
                        elif hardness == 400:
                            hardness = 250
                    if Music_button.left <= newmouse_x <= Music_button.right and Music_button.bottom <= newmouse_y <= Music_button.top:
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE | winsound.SND_ASYNC )
                        if music == 0:
                            music = 1
                        elif music == 1:
                            music = 0
                    if Theme_button.left <= newmouse_x <= Theme_button.right and Theme_button.bottom <= newmouse_y <= Theme_button.top:
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                        if Theme == 0:
                            Theme = 1
                        elif Theme == 1:
                            Theme = 0

            elif game_mode == 2:
                if (active_tank == tank1 and night_slider_left.right - 20 <= newmouse_x <= night_slider_left.right and night_slider_left.bottom <= newmouse_y <= night_slider_left.top):
                    if left_slider_out == 0:
                        left_slider_out = 140
                        wepons_left_out = 100
                    else:
                        left_slider_out = 0
                        wepons_left_out = 0
                    if Sounds == 1:
                        winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                elif (active_tank == tank2 and night_slider_right.left <= newmouse_x <= night_slider_right.left + 20 and night_slider_right.bottom <= newmouse_y <= night_slider_right.top):
                    if right_slider_out == 0:
                        right_slider_out = 140
                        wepons_right_out = 190
                    else:
                        right_slider_out = 0
                        wepons_right_out = 0
                    if Sounds == 1:
                        winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                if (left_slider_out > 0 and night_slider_left.left <= newmouse_x <= night_slider_left.right-25):
                    if (len(active_tank.weapons)>=1 and night_slider_left.top - 8 - 19 * 1 <= newmouse_y <= night_slider_left.top):
                        active_tank.selected_weapon = 0
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons)>=2  and night_slider_left.top - 8 - 19 * 2 <= newmouse_y <= night_slider_left.top - 8 - 19 * 1):
                        active_tank.selected_weapon = 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 3 and night_slider_left.top - 8 - 19 * 3 <= newmouse_y <= night_slider_left.top - 8 - 19 * 2):
                        active_tank.selected_weapon = 2
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 4 and night_slider_left.top - 8 - 19 * 4 <= newmouse_y <= night_slider_left.top - 8 - 19 * 3):
                        active_tank.selected_weapon = 3
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons)>=5  and night_slider_left.top - 8 - 19 * 5 <= newmouse_y <= night_slider_left.top - 8 - 19 * 4):
                        active_tank.selected_weapon = 4
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 6 and night_slider_left.top - 8 - 19 * 6 <= newmouse_y <= night_slider_left.top - 8 - 19 * 5):
                        active_tank.selected_weapon = 5
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 7 and night_slider_left.top - 8 - 19 * 7 <= newmouse_y <= night_slider_left.top - 8 - 19 * 6):
                        active_tank.selected_weapon = 6
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 8 and night_slider_left.top - 8 - 19 * 8 <= newmouse_y <= night_slider_left.top- 8 - 19 * 7):
                        active_tank.selected_weapon = 7
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 9 and night_slider_left.top - 8 - 19 * 9 <= newmouse_y <= night_slider_left.top - 8 - 19 * 8):
                        active_tank.selected_weapon = 8
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 10 and night_slider_left.bottom <= newmouse_y <= night_slider_left.top - 8 - 19 * 9):
                        active_tank.selected_weapon = 9
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                elif (right_slider_out > 0 and night_slider_right.left+25 <= newmouse_x <= night_slider_right.right):
                    if (len(active_tank.weapons)>=1 and night_slider_right.top - 8 - 19 * 1 <= newmouse_y <= night_slider_right.top):
                        active_tank.selected_weapon = 0
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons)>=2 and night_slider_right.top - 8 - 19 * 2 <= newmouse_y <= night_slider_right.top - 8 - 19 * 1):
                        active_tank.selected_weapon = 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 3 and night_slider_right.top - 8 - 19 * 3 <= newmouse_y <= night_slider_right.top - 8 - 19 * 2):
                        active_tank.selected_weapon = 2
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 4 and night_slider_right.top - 8 - 19 * 4 <= newmouse_y <= night_slider_right.top - 8 - 19 * 3):
                        active_tank.selected_weapon = 3
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons)>=5 and night_slider_right.top - 8 - 19 * 5 <= newmouse_y <= night_slider_right.top - 8 - 19 * 4):
                        active_tank.selected_weapon = 4
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 6 and night_slider_right.top - 8 - 19 * 6 <= newmouse_y <= night_slider_right.top - 8 - 19 * 5):
                        active_tank.selected_weapon = 5
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 7 and night_slider_right.top - 8 - 19 * 7 <= newmouse_y <= night_slider_right.top - 8 - 19 * 6):
                        active_tank.selected_weapon = 6
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 8 and night_slider_right.top - 8 - 19 * 8 <= newmouse_y <= night_slider_right.top- 8 - 19 * 7):
                        active_tank.selected_weapon = 7
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 9 and night_slider_right.top - 8 - 19 * 9 <= newmouse_y <= night_slider_right.top - 8 - 19 * 8):
                        active_tank.selected_weapon = 8
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)
                    elif (len(active_tank.weapons) >= 10 and night_slider_right.bottom <= newmouse_y <= night_slider_right.top - 8 - 19 * 9):
                        active_tank.selected_weapon = 9
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_PURGE)

                if Theme == 1:
                    if Fire_Button.left <= newmouse_x <= Fire_Button.right and Fire_Button.bottom <= newmouse_y <= Fire_Button.top:
                        if len(active_tank.weapons) != 0:
                            fire = True
                            if active_tank.weapons[active_tank.selected_weapon] == 0:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/laser1.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 1:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/heq.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_LOOP | winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 2:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/cannonpop.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 3:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/cannonpop.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 4:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/cannonpop.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                    elif move_button.right - move_button.width /     2 <= newmouse_x <= move_button.right and move_button.bottom <= newmouse_y <= move_button.top:
                        left = False
                        right = True
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                        elif move_button.left <= newmouse_x <= move_button.left + move_button.width / 2 and move_button.bottom <= newmouse_y <= move_button.top:
                            right = False
                            left = True
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                        elif Angle_button.right - Angle_button.width / 2 <= newmouse_x <= Angle_button.right and Angle_button.bottom <= newmouse_y <= Angle_button.top:
                            if active_tank.turret_angle == 359:
                                active_tank.turret_angle = 0
                            else:
                                active_tank.turret_angle += 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                        elif Angle_button.left <= newmouse_x <= Angle_button.left + Angle_button.width / 2 and Angle_button.bottom <= newmouse_y <= Angle_button.top:
                            if active_tank.turret_angle == 0:
                                active_tank.turret_angle = 359
                            else:
                                active_tank.turret_angle -= 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                        elif power_slider.right - power_slider.width / 2 <= newmouse_x <= power_slider.right and power_slider.bottom <= newmouse_y <= power_slider.top:
                            if active_tank.power < 100:
                                active_tank.power += 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
                    elif power_slider.left <= newmouse_x <= power_slider.left + power_slider.width / 2 and power_slider.bottom <= newmouse_y <= power_slider.top:
                        if active_tank.power > 0:
                            active_tank.power -= 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                    else:
                        return None
                elif Theme == 0:
                    if FireNight_button.left <= newmouse_x <= FireNight_button.right and FireNight_button.bottom <= newmouse_y <= FireNight_button.top:
                        if len(active_tank.weapons) != 0:
                            fire = True
                            mouse_On = 1
                            if active_tank.weapons[active_tank.selected_weapon] == 5:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/laser1.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 1:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/heq.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_LOOP | winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 2:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/cannonpop.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 3:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/cannonpop.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                            elif active_tank.weapons[active_tank.selected_weapon] == 4:
                                if Sounds == 1:
                                    winsound.PlaySound('Sounds/cannonpop.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)

                    elif moveNight_button.left <= newmouse_x <= moveNight_button.left + 33 and moveNight_button.bottom <= newmouse_y <= moveNight_button.top:
                        left = True
                        right = False
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
                    elif moveNight_button.right - 33 <= newmouse_x <= moveNight_button.right and moveNight_button.bottom <= newmouse_y <= moveNight_button.top:
                        right = True
                        left = False
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
                    elif angle_power_button.left + 32 <= newmouse_x <= angle_power_button.right - 32 and angle_power_button.top - 32 <= newmouse_y <= angle_power_button.top:
                        if active_tank.turret_angle == 359:
                            active_tank.turret_angle = 0
                        else:
                            active_tank.turret_angle += 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
                    elif angle_power_button.left + 32 <= newmouse_x <= angle_power_button.right - 32 and angle_power_button.bottom <= newmouse_y <= angle_power_button.bottom + 32:
                        if active_tank.turret_angle == 0:
                            active_tank.turret_angle = 359
                        else:
                            active_tank.turret_angle -= 1

                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
                    elif angle_power_button.left <= newmouse_x <= angle_power_button.left + 33 and angle_power_button.bottom + 33 <= newmouse_y <= angle_power_button.bottom + 66:
                        active_tank.power -= 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
                    elif angle_power_button.right - 33 <= newmouse_x <= angle_power_button.right and angle_power_button.bottom + 33 <= newmouse_y <= angle_power_button.bottom + 66:
                        active_tank.power += 1
                        if Sounds == 1:
                            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                    elif Exit_button.left <= newmouse_x <= Exit_button.right and Exit_button.bottom <= newmouse_y <= Exit_button.top:
                        if Game_End_subwindow:
                            if Sounds == 1:
                                winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                            sys.exit()
                    elif Newgame_button.left <= newmouse_x <= Newgame_button.right and Newgame_button.bottom <= newmouse_y <= Newgame_button.top:
                        if Game_End_subwindow:
                            init_world_shape()
                            tank1.score = 0
                            tank2.score = 0
                            tank1.pos = [200, 0]
                            tank2.pos = [1080, 0]
                            active_tank = tank1
                            tank1.moves = 6
                            tank2.moves = 6
                            tank1.weapons, tank2.weapons = [randrange(0, 7, 1) for _ in range(10)], [randrange(0, 7, 1) for _ in range(10)]
                            calc_tank1_pos()
                            calc_tank2_pos()
                            projs_init()
                            Resume = 1
                            game_mode = 2
                            Game_End_subwindow = 0
                            if Sounds == 1:
                                winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)


def keyboard(key, x, y):
    global active_tank, fire, right, left, movement, weapon, game_mode, credits_sub_menu
    if time == 0:
        if game_mode == 2:
            if key == b"a" and active_tank.power > 0:
                active_tank.power -= 1
            if key == b"d" and active_tank.power < 100:
                active_tank.power += 1
            if key == b"w":
                if active_tank.turret_angle == 359:
                    active_tank.turret_angle = 0
                else:
                    active_tank.turret_angle += 1
            if key == b"s":
                if active_tank.turret_angle == 0:
                    active_tank.turret_angle = 359
                else:
                    active_tank.turret_angle -= 1
            if key == b"f" and len(tank2.weapons) != 0:
                fire = True
                if active_tank.weapons[active_tank.selected_weapon] == 5:
                    if Sounds == 1:
                        winsound.PlaySound('Sounds/laser1.wav',
                                           winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                elif active_tank.weapons[active_tank.selected_weapon] == 1:
                    if Sounds == 1:
                        winsound.PlaySound('Sounds/cannonpop.wav',
                                           winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                elif active_tank.weapons[active_tank.selected_weapon] == 2:
                    if Sounds == 1:
                        winsound.PlaySound('Sounds/cannonpop.wav',
                                           winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                elif active_tank.weapons[active_tank.selected_weapon] == 3:
                    if Sounds == 1:
                        winsound.PlaySound('Sounds/cannonpop.wav',
                                           winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
                elif active_tank.weapons[active_tank.selected_weapon] == 4:
                    if Sounds == 1:
                        winsound.PlaySound('Sounds/cannonpop.wav',
                                           winsound.SND_FILENAME | winsound.SND_ASYNC |  winsound.SND_PURGE)
            if key == b"c":
                if active_tank.selected_weapon == len(active_tank.weapons) - 1:
                    active_tank.selected_weapon = 0
                else:
                    active_tank.selected_weapon += 1
    if key == b"e":
        if game_mode == 0:
            winsound.PlaySound('Sounds/crick.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
            game_mode = 1
        elif game_mode == 1 and Resume == 1:
            projs_init()
            game_mode = 2
    if key == b"q":
        credits_sub_menu = 0
        if game_mode == 2:
            game_mode = 1
        elif game_mode == 1:
            game_mode = 0


def special_keys(key, x, y):
    global left, right
    if time == 0:
        if game_mode == 2:
            if key == GLUT_KEY_LEFT:
                left = True
                right = False
            if key == GLUT_KEY_RIGHT:
                right = True
                left = False


###############################################################################
########################## WEAPONS AND COLLISION ##############################
###############################################################################

def displacement(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)


def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def collision_test_tank(projectile):
    if displacement(projectile.x, projectile.y, other_tank.pos[0], other_tank.pos[1]) > 40:
        return False
    else:
        v1 = [cos(radians(other_tank.tank_angle)), sin(radians(other_tank.tank_angle))]
        v2 = [sin(radians(other_tank.tank_angle)), -cos(radians(other_tank.tank_angle))]
        p1 = [1, 0]
        p2 = [0, 1]

        proj_coords = [[projectile.x + projectile.width / 2, projectile.y + projectile.height / 2],
                       [projectile.x - projectile.width / 2, projectile.y - projectile.height / 2]]
        tank_coords = [[20, 10],[- 20, 10], [- 20, 10],[20, - 10]]
        for i in range(4):
            x1 = tank_coords[i][0] * cos(radians(other_tank.tank_angle)) - tank_coords[i][1] * sin(radians(other_tank.tank_angle))
            y1 = tank_coords[i][0] * sin(radians(other_tank.tank_angle)) + tank_coords[i][1] * cos(radians(other_tank.tank_angle))
            tank_coords[i] = [x1 + other_tank.pos[0], y1 + other_tank.pos[1]]

        axes = [v1, v2, p1, p2]
        for axis in axes:
            L = []
            for coord in tank_coords:
                L.append(dot_product(axis, coord))
            L2 = L[:]
            L.sort()
            min1 = L[0]
            max1 = L[-1]
            
            L = []
            for coord in proj_coords:
                L.append(dot_product(axis, coord))
            L2 = L[:]
            L.sort()
            min2 = L[0]
            max2 = L[-1]
            
            if (min2 > max1 or min1 > max2):
                return False
        return True


def collision_test_world(projectile):
    try:
        if active_tank.selected_weapon == 4:
            state = time > 2.75 and abs((projectile.y - f(projectile.x))) < 9
        else:
            state = time > 0.75 and abs((projectile.y - f(projectile.x))) < 7
        return state
    except ValueError:
        pass


def projs_init():
    global single_shot_projectile, bazooka_projectile, three_shot_projectile_1, three_shot_projectile_2, three_shot_projectile_3, \
        tommy_gun_projectile_1, tommy_gun_projectile_2, tommy_gun_projectile_3, tommy_gun_projectile_4, tommy_gun_projectile_5, tommy_gun_projectile_6, tommy_gun_projectile_7, \
        tommy_gun_projectile_8,     tommy_gun_random_powers, tommy_gun_random_angles, super_lazer_projectile, skipper_projectile, skipper_projectile_2, skipper_projectile_3, \
        acid_rain_projectile, acid_rain_small_projectile_1, acid_rain_small_projectile_2, acid_rain_small_projectile_3, acid_rain_small_projectile_4, acid_rain_small_projectile_5
    single_shot_projectile = Rectangle(40, 40, (-5, -5), 0, "FFFFFF")  # single shot
    bazooka_projectile = Rectangle(14 * 4, 3 * 4, (-5, -5), 0, "FFFFFF")  # bazooka
    super_lazer_projectile = Rectangle(14, 3, (-5, -5), 0, "FFFFFF")  # super lazer
    three_shot_projectile_1 = Rectangle(10, 11, (-5, -5), 0, "FFFFFF")  # 3 shot - 1
    three_shot_projectile_2 = Rectangle(10, 11, (-5, -5), 0, "FFFFFF")  # 3 shot - 2
    three_shot_projectile_3 = Rectangle(10, 11, (-5, -5), 0, "FFFFFF")  # 3 shot - 3
    skipper_projectile = Rectangle(15, 16, (-5, -5), 0, "FFFFFF")
    skipper_projectile_2 = Rectangle(15, 16, (-5, -5), 0, "FFFFFF")
    skipper_projectile_3 = Rectangle(15, 16, (-5, -5), 0, "FFFFFF")
    tommy_gun_projs = []
    for i in range(8):  # tommy gun 8 projectiles
        tommy_gun_projs.append(Rectangle(10, 11, (-5, -5), 0, "EEEEEE"))
    tommy_gun_projectile_1, tommy_gun_projectile_2, tommy_gun_projectile_3, tommy_gun_projectile_4, tommy_gun_projectile_5, tommy_gun_projectile_6 \
        , tommy_gun_projectile_7, tommy_gun_projectile_8 = tommy_gun_projs
    tommy_gun_random_powers = [randrange(-4, 5, 1) for _ in range(8)]
    tommy_gun_random_angles = [randrange(-4, 5, 1) for _ in range(8)]

    acid_rain_projectile = Rectangle(200 / 2, 37 / 2, (-5, -5), 0, "FFFFFF")
    acid_rain_small_projectile_1 = Rectangle(2, 2, (-5, -5), 0, "000000")
    acid_rain_small_projectile_2 = Rectangle(2, 2, (-5, -5), 0, "000000")
    acid_rain_small_projectile_3 = Rectangle(2, 2, (-5, -5), 0, "000000")
    acid_rain_small_projectile_4 = Rectangle(2, 2, (-5, -5), 0, "000000")
    acid_rain_small_projectile_5 = Rectangle(2, 2, (-5, -5), 0, "000000")


def skipper(tank):
    global time, time2, skipper_projectile, skipper_c, diameters
    if not collision_test_world(skipper_projectile):
        if not collision_test_tank(skipper_projectile):
            vx = tank.power * 1.1 * cos(radians(tank.turret_angle))
            vy = tank.power * 1.1 * sin(radians(tank.turret_angle))
            dx = vx * time
            dy = (vy * time) - 4.9 * (time ** 2)
            skipper_projectile.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx
            skipper_projectile.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy
            shot_tex.draw_tex()
            skipper_projectile.build_center()
        else:
            draw_circle(0, 6.5, diameters[0], skipper_projectile.x, skipper_projectile.y)
            active_tank.score += 2.5
            diameters[0] += 1
    else:
        if not (time2[0] > 4 and collision_test_world(skipper_projectile_2)):
            if not collision_test_tank(skipper_projectile_2):
                vx = tank.power * 0.7 * cos(radians(tank.turret_angle))
                vy = tank.power * 0.7 * sin(radians(tank.turret_angle))
                dx = vx * time2[0]
                dy = (vy * time2[0]) - 4.9 * (time2[0] ** 2)
                skipper_projectile_2.x = skipper_projectile.x + dx
                skipper_projectile_2.y = skipper_projectile.y + dy
                shot2_tex.draw_tex()
                skipper_projectile_2.build_center()
                time2[0] += 0.25
            else:
                draw_circle(0, 6.5, diameters[1], skipper_projectile_2.x, skipper_projectile_2.y)
                diameters[1] += 0.4
                active_tank.score += 2
        else:
            if not (time2[1]>4 and collision_test_tank(skipper_projectile_3)):
                vx = tank.power * 0.55 * cos(radians(tank.turret_angle))
                vy = tank.power * 0.55 * sin(radians(tank.turret_angle))
                dx = vx * time2[1]
                dy = (vy * time2[1]) - 4.9 * (time2[1] ** 2)
                skipper_projectile_3.x = skipper_projectile_2.x + dx
                skipper_projectile_3.y = skipper_projectile_2.y + dy
                shot3_tex.draw_tex()
                skipper_projectile_3.build_center()
                time2[1] += 0.25
            else:
                draw_circle(0, 6.5, diameters[2], skipper_projectile_3.x, skipper_projectile_3.y)
                diameters[2] += 0.8
                active_tank.score += 2

    time += 0.25


def throw_single_shot(tank):
    global time, single_shot_projectile, other_tank
    if not collision_test_world(single_shot_projectile):
        if not collision_test_tank(single_shot_projectile):
            vx = tank.power * 1.1 * cos(radians(tank.turret_angle))
            vy = tank.power * 1.1 * sin(radians(tank.turret_angle))

            dx = vx * time
            dy = (vy * time) - 4.9 * (time ** 2)

            single_shot_projectile.angle += 20

            single_shot_projectile.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx
            single_shot_projectile.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy
            single_shot_tex.draw_tex()
            single_shot_projectile.build_center()
        else:
            draw_circle(0, 6.5, diameters[0], single_shot_projectile.x, single_shot_projectile.y)
            if Sounds == 1:
                winsound.PlaySound('Sounds/hwa7.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
            diameters[0] += 1
            active_tank.score += 6
    else:
        winsound.PlaySound('Sounds/null.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_PURGE)
        draw_circle(0, 6.5, diameters[0], single_shot_projectile.x, single_shot_projectile.y)
        diameters[0] += 1
        dis = displacement(single_shot_projectile.x, single_shot_projectile.y, *other_tank.pos)
        if dis < 80:
            if other_tank == tank2:
                if single_shot_projectile.x > tank2.pos[0]:
                    tank2.pos[0] += 19
                    calc_tank2_pos()
                elif single_shot_projectile.x < tank2.pos[0]:
                    tank2.pos[0] += 21
                    calc_tank2_pos()
            elif other_tank == tank1:
                if single_shot_projectile.x > tank1.pos[0]:
                    tank1.pos[0] -= 21
                    calc_tank1_pos()
                elif single_shot_projectile < tank1.pos[0]:
                    tank1.pos[0] -= 19
                    calc_tank1_pos()
            active_tank.score += 0.8
    time += 0.25


def shoot_bazooka(tank):
    global time, bazooka_projectile, diameters, active_tank
    if not collision_test_world(bazooka_projectile):
        if not collision_test_tank(bazooka_projectile):
            dx = time * cos(radians(tank.turret_angle)) * tank.power
            dy = time * sin(radians(tank.turret_angle)) * tank.power

            bazooka_projectile.angle = tank.turret_angle
            bazooka_projectile.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx
            bazooka_projectile.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy

            bazooka_tex.draw_tex()
            bazooka_projectile.build_corner()
        else:
            draw_circle(0, 6.5, diameters[0], bazooka_projectile.x, bazooka_projectile.y)
            diameters[0] += 1
            active_tank.score += 3.5
    else:
        draw_circle(0, 6.5, diameters[0], bazooka_projectile.x, bazooka_projectile.y)
        diameters[0] += 1
        dis = displacement(single_shot_projectile.x, single_shot_projectile.y, *other_tank.pos)
        if dis < 80:
            if other_tank == tank2:
                if single_shot_projectile.x > tank2.pos[0]:
                    tank2.pos[0] += 19
                    calc_tank2_pos()
                elif single_shot_projectile.x < tank2.pos[0]:
                    tank2.pos[0] += 21
                    calc_tank2_pos()
            elif other_tank == tank1:
                if single_shot_projectile.x > tank1.pos[0]:
                    tank1.pos[0] -= 21
                    calc_tank1_pos()
                elif single_shot_projectile < tank1.pos[0]:
                    tank1.pos[0] -= 19
                    calc_tank1_pos()
            active_tank.score += 1.2

    time += 0.25


def shoot_super_lazer(tank):
    global time, super_lazer_projectile, diameters, active_tank

    if not collision_test_tank(super_lazer_projectile):
        dx = time * cos(radians(tank.turret_angle)) * tank.power * 1.5
        dy = time * sin(radians(tank.turret_angle)) * tank.power * 1.5

        super_lazer_projectile.angle = tank.turret_angle
        super_lazer_projectile.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx
        super_lazer_projectile.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy

        Color = [int(dx * dy % 256), int(2 * dx % 256), int(dx ** 2 % 256)]
        Color = hex_color(Color)

        if active_tank == tank1:
            super_lazer_null_projectile = Rectangle(super_lazer_projectile.width + dx, 5,
            [tank.pos[0] + 24 * cos(radians(tank.turret_angle)),
             tank.pos[1] + 24 * sin(radians(tank.turret_angle))],
             tank.turret_angle, Color)
        else:
            super_lazer_null_projectile = Rectangle(super_lazer_projectile.width - dx, 5,
                                                    [tank.pos[0] + 24 * cos(radians(tank.turret_angle)),
                                                     tank.pos[1] + 24 * sin(radians(tank.turret_angle))],
                                                    tank.turret_angle, Color)
        super_lazer_null_projectile.build_corner()

    else:
        winsound.PlaySound('Sounds/ayyy.wav', winsound.SND_FILENAME | winsound.SND_PURGE | winsound.SND_ASYNC |  winsound.SND_LOOP )
        draw_circle(0, 6.5, diameters[0], super_lazer_projectile.x, super_lazer_projectile.y)
        diameters[0] += 1
        active_tank.score += 3.5

    time += 0.25


def throw_three_shot(tank):
    global time, three_shot_projectile_1, three_shot_projectile_2, three_shot_projectile_3, diameters
    if not collision_test_world(three_shot_projectile_1):
        if not collision_test_tank(three_shot_projectile_1):
            vx1 = tank.power * 1.1 * cos(radians(tank.turret_angle))
            vy1 = tank.power * 1.1 * sin(radians(tank.turret_angle))
            dx1 = vx1 * time
            dy1 = (vy1 * time) - 4.9 * (time ** 2)
            three_shot_projectile_1.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx1
            three_shot_projectile_1.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy1
            shot_tex.draw_tex()
            three_shot_projectile_1.build_center()
        else:
            draw_circle(0, 6.5, diameters[0], three_shot_projectile_1.x, three_shot_projectile_1.y)
            diameters[0] += 0.5
            active_tank.score += 2

    if not collision_test_world(three_shot_projectile_2):
        if not collision_test_tank(three_shot_projectile_2):
            vx2 = tank.power * 1.1 * cos(radians(tank.turret_angle + 2))
            vy2 = tank.power * 1.1 * sin(radians(tank.turret_angle + 2))
            dx2 = vx2 * time
            dy2 = (vy2 * time) - 4.9 * (time ** 2)
            three_shot_projectile_2.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx2
            three_shot_projectile_2.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy2
            shot_tex.draw_tex()
            three_shot_projectile_2.build_center()
        else:
            draw_circle(0, 6.5, diameters[1], three_shot_projectile_2.x, three_shot_projectile_2.y)
            diameters[1] += 0.5
            active_tank.score += 2

    if not collision_test_world(three_shot_projectile_3):
        if not collision_test_tank(three_shot_projectile_3):
            vx3 = tank.power * 1.1 * cos(radians(tank.turret_angle - 2))
            vy3 = tank.power * 1.1 * sin(radians(tank.turret_angle - 2))
            dx3 = vx3 * time
            dy3 = (vy3 * time) - 4.9 * (time ** 2)
            three_shot_projectile_3.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx3
            three_shot_projectile_3.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy3
            shot_tex.draw_tex()
            three_shot_projectile_3.build_center()
        else:
            draw_circle(0, 6.5, diameters[2], three_shot_projectile_3.x, three_shot_projectile_3.y)
            diameters[2] += 0.5
            active_tank.score += 2

    time += .25


def shoot_tommy_gun(tank):
    global time, tommy_gun_projectile_1, tommy_gun_projectile_2, tommy_gun_projectile_3, tommy_gun_projectile_4, tommy_gun_projectile_5, \
        tommy_gun_projectile_6, tommy_gun_projectile_7, tommy_gun_projectile_8
    if not collision_test_world(tommy_gun_projectile_1):
        vx1 = (tank.power + tommy_gun_random_powers[0]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[0]))
        vy1 = (tank.power + tommy_gun_random_powers[0]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[0]))
        dx1 = vx1 * time
        dy1 = (vy1 * time) - 4.9 * (time ** 2)
        tommy_gun_projectile_1.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx1
        tommy_gun_projectile_1.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy1
        if not collision_test_tank(tommy_gun_projectile_1):
            shot_tex.draw_tex()
            tommy_gun_projectile_1.build_center()
        else:
            active_tank.score += 4

    if time >= 1:
        if not collision_test_world(tommy_gun_projectile_2):
            vx2 = (tank.power + tommy_gun_random_powers[1]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[1]))
            vy2 = (tank.power + tommy_gun_random_powers[1]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[1]))
            dx2 = vx2 * (time - 1)
            dy2 = (vy2 * (time - 1)) - 4.9 * ((time - 1) ** 2)
            tommy_gun_projectile_2.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx2
            tommy_gun_projectile_2.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy2
            if not collision_test_tank(tommy_gun_projectile_2):
                shot_tex.draw_tex()
                tommy_gun_projectile_2.build_center()
            else:
                active_tank.score += 4
    if time >= 2:
        if not collision_test_world(tommy_gun_projectile_3):
            vx3 = (tank.power + tommy_gun_random_powers[2]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[2]))
            vy3 = (tank.power + tommy_gun_random_powers[2]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[2]))
            dx3 = vx3 * (time - 2)
            dy3 = (vy3 * (time - 2)) - 4.9 * ((time - 2) ** 2)
            tommy_gun_projectile_3.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx3
            tommy_gun_projectile_3.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy3
            if not collision_test_tank(tommy_gun_projectile_3):
                shot_tex.draw_tex()
                tommy_gun_projectile_3.build_center()
            else:
                active_tank.score += 4
    if time>=3:
        if not collision_test_world(tommy_gun_projectile_4):
            vx4 = (tank.power + tommy_gun_random_powers[3]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[3]))
            vy4 = (tank.power + tommy_gun_random_powers[3]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[3]))
            dx4 = vx4 * (time - 3)
            dy4 = (vy4 * (time - 3)) - 4.9 * ((time - 3) ** 2)
            tommy_gun_projectile_4.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx4
            tommy_gun_projectile_4.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy4
            if not collision_test_tank(tommy_gun_projectile_4):
                shot_tex.draw_tex()
                tommy_gun_projectile_4.build_center()
            else:
                active_tank.score += 4
    if time >=4:
        if not collision_test_world(tommy_gun_projectile_5):
            vx5 = (tank.power + tommy_gun_random_powers[4]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[4]))
            vy5 = (tank.power + tommy_gun_random_powers[4]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[4]))
            dx5 = vx5 * (time - 4)
            dy5 = (vy5 * (time - 4)) - 4.9 * ((time - 4) ** 2)
            tommy_gun_projectile_5.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx5
            tommy_gun_projectile_5.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy5
            if not collision_test_tank(tommy_gun_projectile_5):
                shot_tex.draw_tex()
                tommy_gun_projectile_5.build_center()
            else:
                active_tank.score += 4
    if time >= 5:
        if not collision_test_world(tommy_gun_projectile_6):
            vx6 = (tank.power + tommy_gun_random_powers[5]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[5]))
            vy6 = (tank.power + tommy_gun_random_powers[5]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[5]))
            dx6 = vx6 * (time - 5)
            dy6 = (vy6 * (time - 5)) - 4.9 * ((time - 5) ** 2)
            tommy_gun_projectile_6.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx6
            tommy_gun_projectile_6.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy6
            if not collision_test_tank(tommy_gun_projectile_6):
                shot_tex.draw_tex()
                tommy_gun_projectile_6.build_center()
            else:
                active_tank.score += 4
    if time >= 6:
        if not collision_test_world(tommy_gun_projectile_7):
            vx7 = (tank.power + tommy_gun_random_powers[6]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[6]))
            vy7 = (tank.power + tommy_gun_random_powers[6]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[6]))
            dx7 = vx7 * (time - 6)
            dy7 = (vy7 * (time - 6)) - 4.9 * ((time - 6) ** 2)
            tommy_gun_projectile_7.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx7
            tommy_gun_projectile_7.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy7
            if not collision_test_tank(tommy_gun_projectile_7):
                shot_tex.draw_tex()
                tommy_gun_projectile_7.build_center()
            else:
                active_tank.score += 4
    if time >= 7:
        if not collision_test_world(tommy_gun_projectile_8):
            vx8 = (tank.power + tommy_gun_random_powers[7]) * 1.1 * cos(radians(tank.turret_angle + tommy_gun_random_angles[7]))
            vy8 = (tank.power + tommy_gun_random_powers[7]) * 1.1 * sin(radians(tank.turret_angle + tommy_gun_random_angles[7]))
            dx8 = vx8 * (time - 7)
            dy8 = (vy8 * (time - 7)) - 4.9 * ((time - 7) ** 2)
            tommy_gun_projectile_8.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx8
            tommy_gun_projectile_8.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy8
            if not collision_test_tank(tommy_gun_projectile_8):
                shot_tex.draw_tex()
                tommy_gun_projectile_8.build_center()
            else:
                active_tank.score += 4

    time += 0.2


def throw_acid_rain(tank):
    global time, time2, acid_rain_projectile, acid_rain_small_projectile_1, acid_rain_small_projectile_2, acid_rain_small_projectile_3, acid_rain_small_projectile_4, acid_rain_small_projectile_5

    if abs(acid_rain_projectile.x - other_tank.pos[0]) > 12:
        vx = tank.power * 1.1 * cos(radians(tank.turret_angle))
        vy = tank.power * 1.1 * sin(radians(tank.turret_angle))
        dx = vx * time
        dy = (vy * time) - 4.9 * (time ** 2)
        acid_rain_projectile.x = tank.pos[0] + 24 * cos(radians(tank.turret_angle)) + dx
        acid_rain_projectile.y = tank.pos[1] + 24 * sin(radians(tank.turret_angle)) + dy
        acid_rain_tex.draw_tex()
        if not collision_test_world(acid_rain_projectile):
            acid_rain_projectile.build_center()

    elif acid_rain_projectile.y - other_tank.pos[1] > 5:
        acid_rain_small_projectile_1.x = other_tank.pos[0] - 20
        acid_rain_small_projectile_2.x = other_tank.pos[0] - 10
        acid_rain_small_projectile_3.x = other_tank.pos[0]
        acid_rain_small_projectile_4.x = other_tank.pos[0] + 10
        acid_rain_small_projectile_5.x = other_tank.pos[0] + 20
        dy = -4.5 * time2[0] ** 2
        acid_rain_small_projectile_1.y = acid_rain_projectile.y + dy
        shot_tex.draw_tex()
        acid_rain_small_projectile_1.build_center()
        if not collision_test_tank(acid_rain_small_projectile_1):
            acid_rain_small_projectile_1.build_center()
        else:
            active_tank.score += 4
        acid_rain_small_projectile_2.y = acid_rain_projectile.y + 1.1 * dy
        if not collision_test_tank(acid_rain_small_projectile_2):
            acid_rain_small_projectile_2.build_center()
        else:
            active_tank.score += 4
        acid_rain_small_projectile_3.y = acid_rain_projectile.y + 1.2 * dy
        if not collision_test_tank(acid_rain_small_projectile_3):
            acid_rain_small_projectile_3.build_center()
        else:
            active_tank.score += 4
        acid_rain_small_projectile_4.y = acid_rain_projectile.y + 1.3 * dy
        if not collision_test_tank(acid_rain_small_projectile_4):
            acid_rain_small_projectile_4.build_center()
        else:
            active_tank.score += 4
        acid_rain_small_projectile_5.y = acid_rain_projectile.y + 1.4 * dy
        if not collision_test_tank(acid_rain_small_projectile_5):
            acid_rain_small_projectile_5.build_center()
        else:
            active_tank.score += 4
        time2[0] += 0.25
    time += .25


""" Displays modes.
# tanks
"""


def game_options_display():
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    init_tex(game_mode2_bg_tex, game_mode2_bg)
    init_tex(Startgame_button_tex, Startgame_button)
    if Resume == 1:
        init_tex(Resumegame_button_tex, Resumegame_button)
    init_tex(Audio_button_tex, Audio_button)
    init_tex(Music_button_tex, Music_button)
    init_tex(Settings_button_tex, Settings_button)
    init_tex(HTP_button_tex, HTP_button)
    init_tex(HE_MODES_button_tex, HE_MODES_button)
    init_tex(Theme_button_tex, Theme_button)
    if hardness == 250:
        init_tex(Easy_text_tex, Easy_text)
    elif hardness == 400:
        init_tex(Hard_text_tex, Hard_text)
    if Theme == 1:
        init_tex(day_text_tex, day_text)
    else:
        init_tex(night_text_tex, night_text)
    if credits_sub_menu == 1:
        init_tex(subwindow_credits_tex, subwindow_credits)
    glutSwapBuffers()


def display():
    global tank1, tank2, fire, time, time2, right, left, movement, active_tank, other_tank, acid_rain_projectile, diameters, clouds_x, WINDOW_WIDTH, WINDOW_HEIGHT, Theme, Game_End_subwindow, left_slider_out, right_slider_out, night_slider_left, night_slider_right, wepons_left_out, wepons_right_out, weapons_bazooka, weapons_three_shot, weapons_tommy_gun, weapons_acid_rain, weapons_super_lazer, weapons_skipper, weapons_single_shot
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    if right and movement > 0:
        move_right()
        movement -= 1
    elif left and movement > 0:
        move_left()
        movement -= 1
    elif movement == 0:
        right = False
        left = False
        movement = 40
        active_tank.moves -= 1

    if active_tank.moves <= 0:
        moving_var_tank = 0
    else:
        moving_var_tank = active_tank.moves

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if Theme == 1:
        init_tex(background_main_tex, background)
        if -241 <= clouds_x <= 1552:
            clouds_x += 5
        else:
            clouds_x = 0
        clouds = Object(241, 37, -250 + clouds_x, 500, 1)
        init_tex(clouds_tex, clouds)
    elif Theme == 0:
        init_tex(background2_main_tex, background)

    if time != 0:
        glutSetCursor(GLUT_CURSOR_WAIT)
    else:
        glutSetCursor(GLUT_CURSOR_INHERIT)

    if fire:
        if time <= weapon_time[active_tank.weapons[active_tank.selected_weapon]]:
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            if active_tank.weapons[active_tank.selected_weapon] == 0:
                shoot_bazooka(active_tank)
            elif active_tank.weapons[active_tank.selected_weapon] == 1:
                throw_single_shot(active_tank)
            elif active_tank.weapons[active_tank.selected_weapon] == 2:
                throw_three_shot(active_tank)
            elif active_tank.weapons[active_tank.selected_weapon] == 3:
                shoot_tommy_gun(active_tank)
            elif active_tank.weapons[active_tank.selected_weapon] == 4:
                throw_acid_rain(active_tank)
            elif active_tank.weapons[active_tank.selected_weapon] == 5:
                shoot_super_lazer(active_tank)
            elif active_tank.weapons[active_tank.selected_weapon] == 6:
                skipper(active_tank)

        else:
            fire = False
            time = 0
            time2 = [0, 0, 0, 0]
            active_tank.weapons.pop(active_tank.selected_weapon)
            active_tank.selected_weapon = 0
            diameters = [0, 0, 0]
            projs_init()
            if active_tank == tank1:
                active_tank = tank2
                other_tank = tank1
                left_slider_out = 0
                wepons_left_out = 0
            elif active_tank == tank2:
                active_tank = tank1
                other_tank = tank2
                right_slider_out = 0
                wepons_right_out = 0

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor(Color('2ecc71'))
    draw_world()

    tank1_tex.draw_tex()
    tank1.build()

    tank2_tex.draw_tex()
    tank2.build()

    # Start drawing Gui Textures
    glLoadIdentity()

    day_slider_left = Object(200, 200, -180 + left_slider_out, 388, 1)
    day_slider_right = Object(200, 200, 1260 - right_slider_out, 388, 1)
    night_slider_left = Object(200, 200, -180 + left_slider_out, 388, 1)
    night_slider_right = Object(200, 200, 1260 - right_slider_out, 388, 1)

    if Theme == 1:
        init_tex(bg_D_tex, Gui_Panel)
        init_tex(fire_button_tex, Fire_Button)
        init_tex(move_button_tex, move_button)
        init_tex(Angle_button_tex, Angle_button)
        init_tex(Power_slider_tex, power_slider)
        if active_tank == tank1:
            init_tex(day_slider_left_tex, day_slider_left)
        else:
            init_tex(day_slider_right_tex, day_slider_right)

    elif Theme == 0:
        # replace with new icons
        init_tex(bg_N_tex, Gui_Panel)
        init_tex(angle_power_tex, angle_power_button)
        init_tex(Fire_tex, FireNight_button)
        init_tex(move_tex, moveNight_button)
        if active_tank == tank1:
            init_tex(night_slider_left_tex, night_slider_left)
        else:
            init_tex(night_slider_right_tex, night_slider_right)

    if active_tank == tank1:
        for i in range(len(tank1.weapons)):
            if tank1.weapons[i] == 0:
                weapons_bazooka = Object(90, 14, -90 + wepons_left_out, 566 - i*19, 1)
                init_tex(weapons_bazooka_tex, weapons_bazooka, 1, 0, 0, 0, 1, 1, tank1.selected_weapon != i)
                weapons_icon_bazooka = Object(14, 14, -95 + 2*wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_icon_bazooka_tex, weapons_icon_bazooka)
            elif tank1.weapons[i] == 1:
                #weapon_matrix[tank1.weapons[i]] == 1
                weapons_single_shot = Object(90, 14, -90 + wepons_left_out, 566 - i*19, 1)
                init_tex(weapons_single_shot_tex, weapons_single_shot,1,0,0,0,1,1, tank1.selected_weapon != i)
                weapons_icon_single_shot = Object(14, 14, -95 + 2*wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_icon_single_shot_tex, weapons_icon_single_shot)
            elif tank1.weapons[i] == 2:
                weapons_three_shot = Object(90, 14, -90 + wepons_left_out, 566 - i*19, 1)
                init_tex(weapons_three_shot_tex, weapons_three_shot,1,0,0,0,1,1, tank1.selected_weapon != i)
                weapons_icon_three_shot = Object(14, 14, -95 + 2*wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_icon_three_shot_tex, weapons_icon_three_shot)
            elif tank1.weapons[i] == 3:
                weapons_tommy_gun = Object(90, 14, -90 + wepons_left_out, 566 - i*19, 1)
                init_tex(weapons_tommy_gun_tex, weapons_tommy_gun,1,0,0,0,1,1, tank1.selected_weapon != i)
                weapons_icon_tommy_gun = Object(14, 14, -95 + 2*wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_icon_tommy_gun_tex, weapons_icon_tommy_gun)
            elif tank1.weapons[i] == 4:
                weapons_acid_rain = Object(90, 14, -90 + wepons_left_out, 566 - i*19, 1)
                init_tex(weapons_acid_rain_tex, weapons_acid_rain,1,0,0,0,1,1, tank1.selected_weapon != i)
                weapons_icon_acid_rain = Object(14, 14, -95 + 2*wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_icon_acid_rain_tex, weapons_icon_acid_rain)
            elif tank1.weapons[i] == 5:
                weapons_super_lazer = Object(90, 14, -90 + wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_super_lazer_tex, weapons_super_lazer,1,0,0,0,1,1, tank1.selected_weapon != i)
                weapons_icon_super_lazer = Object(14, 14, -95 + 2*wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_icon_super_lazer_tex, weapons_icon_super_lazer)
            else:
                weapons_skipper = Object(90, 14, -90 + wepons_left_out, 566 - i*19, 1)
                init_tex(weapons_skipper_tex, weapons_skipper,1,0,0,0,1,1, tank1.selected_weapon != i)
                weapons_icon_skipper = Object(14, 14, -95 + 2*wepons_left_out, 566 - i * 19, 1)
                init_tex(weapons_icon_skipper_tex, weapons_icon_skipper)

    if active_tank == tank2:
        for i in range(len(tank2.weapons)):
            if tank2.weapons[i] == 0:
                weapons_bazooka = Object(90, 14, 1370 - wepons_right_out, 566 - i*19, 1)
                init_tex(weapons_bazooka_tex, weapons_bazooka,1,0,0,0, tank2.selected_weapon != i,1,1)
                weapons_icon_bazooka = Object(14, 14, 1356 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_icon_bazooka_tex, weapons_icon_bazooka)
            elif tank2.weapons[i] == 1:
                weapons_single_shot = Object(90, 14, 1370 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_single_shot_tex, weapons_single_shot, 1, 0, 0, 0, tank2.selected_weapon != i, 1, 1)
                weapons_icon_single_shot = Object(14, 14, 1356 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_icon_single_shot_tex, weapons_icon_single_shot)
            elif tank2.weapons[i] == 2:
                weapons_three_shot = Object(90, 14, 1370 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_three_shot_tex, weapons_three_shot, 1, 0, 0, 0, tank2.selected_weapon != i, 1, 1)
                weapons_icon_three_shot = Object(14, 14, 1356 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_icon_three_shot_tex, weapons_icon_three_shot)
            elif tank2.weapons[i] == 3:
                weapons_tommy_gun = Object(90, 14, 1370 - wepons_right_out, 566 - i*19, 1)
                init_tex(weapons_tommy_gun_tex, weapons_tommy_gun,1,0,0,0, tank2.selected_weapon != i,1,1)
                weapons_icon_tommy_gun = Object(14, 14, 1356 - wepons_right_out, 566 - i*19, 1)
                init_tex(weapons_icon_tommy_gun_tex, weapons_icon_tommy_gun)
            elif tank2.weapons[i] == 4:
                weapons_acid_rain = Object(90, 14, 1370 - wepons_right_out, 566 - i*19, 1)
                init_tex(weapons_acid_rain_tex, weapons_acid_rain,1,0,0,0, tank2.selected_weapon != i,1,1)
                weapons_icon_acid_rain = Object(14, 14, 1356 - wepons_right_out, 566 - i*19, 1)
                init_tex(weapons_icon_acid_rain_tex, weapons_icon_acid_rain)
            elif tank2.weapons[i] == 5:
                weapons_super_lazer = Object(90, 14, 1370 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_super_lazer_tex, weapons_super_lazer,1,0,0,0, tank2.selected_weapon != i,1,1)
                weapons_icon_super_lazer = Object(14, 14, 1356 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_icon_super_lazer_tex, weapons_icon_super_lazer)
            else:
                weapons_skipper = Object(90, 14, 1370 - wepons_right_out, 566 - i*19, 1)
                init_tex(weapons_skipper_tex, weapons_skipper,1,0,0,0, tank2.selected_weapon != i,1,1)
                weapons_icon_skipper = Object(14, 14, 1356 - wepons_right_out, 566 - i * 19, 1)
                init_tex(weapons_icon_skipper_tex, weapons_icon_skipper)


    """ Draw game texts
    """
    if Theme == 0:
        init_tex(player_1_night_tex, player_1_night)
        draw_text(str(int(tank1.score)), 78, 610, 0.25, Color("EEEEEE"))
        init_tex(player_2_night_tex, player_2_night)
        draw_text(str(int(tank2.score)), 1180, 610, 0.25, Color("EEEEEE"))
    else:
        init_tex(player_1_day_tex, player_1_day)
        draw_text(str(int(tank1.score)), 78, 610, 0.25, Color("222222"))
        init_tex(player_2_day_tex, player_2_day)
        draw_text(str(int(tank2.score)), 1180, 610, 0.25, Color("222222"))

    if Theme == 1:
        draw_text(str(active_tank.turret_angle), Angle_button.left + Angle_button.width / 2,
                  Angle_button.bottom + Angle_button.height / 2, 0.1, (0, 0, 0))
        draw_text(str(moving_var_tank), move_button.left + move_button.width / 2,
                  move_button.bottom + move_button.height / 2, 0.1, (0, 0, 0))
        draw_text(str(active_tank.power), power_slider.left + power_slider.width / 2,
                  power_slider.bottom + power_slider.height / 2, 0.1, (0, 0, 0))
        glLoadIdentity()

    elif Theme == 0:
        draw_text(str(active_tank.turret_angle), 1230, 70, 0.1, (1, 1, 1))
        draw_text(str(moving_var_tank), 674, 100, 0.1, (1, 1, 1))
        draw_text(str(active_tank.power), 1165, 70, 0.1, (1, 1, 1))

    if Game_End_subwindow == 1:
        init_tex(Game_End_subwindow_tex, Game_End_subwindows)
        init_tex(Startgame_button_tex, Newgame_button)
        init_tex(Exit_button_tex, Exit_button)

    if len(tank2.weapons) == 0:  #game has ended
        if Theme == 0:
            Game_End_subwindow = 1

        if tank1.score > tank2.score:
            draw_text(tank1.name + " wins!", 510, 500, 0.4, Color("FFFFFF"))
        elif tank1.score < tank2.score:
            draw_text(tank2.name + " wins!", 510, 500, 0.4, Color("FFFFFF"))
        else:
            draw_text("It's a tie!", 510, 500, 0.4, Color("FFFFFF"))


    glutSwapBuffers()


""" Switching Displays
game_mode = 0 for Splash
game_mode = 1 for Options
game_mode = 2 for Game
"""


def switch():
    global game_mode
    if game_mode == 0:
        x = splash_display()
    elif game_mode == 1:
        x = game_options_display()
    elif game_mode == 2:
        x = display()
    return x


def resize(WINDOW_WIDTH, WINDOW_HEIGHT):
    glutReshapeWindow(1280, 720)


def run():
    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b'Pocket Tanks')
    glutInitWindowPosition(0, 0)
    glutReshapeFunc(resize)
    glutDisplayFunc(switch)
    glutIdleFunc(switch)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouseonclick)
    glutPassiveMotionFunc(mouse_motion)
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)  # l,r,b,t,n,f
    glutMainLoop()


run()
