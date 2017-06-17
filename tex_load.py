from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from Gui import *


class Texture:
    def __init__(self, file_name):
        self.file_name = file_name
        self.width = 0
        self.height = 0

    def load(self):
        self.img = Image.open(self.file_name)
        self.data = self.img.tobytes("raw", "RGBA", 0, -1)
        self.width, self.height = self.img.size

    def draw_tex(self):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)

        glEnable(GL_TEXTURE_2D)

        glEnable(GL_BLEND)     # Turn Blending On
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# initializing the textures after loading


def DrawRectangle(rect, a=1, x=0, y=0, z=0, r=1, g=1, b=1):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor(r, g, b, a)
    glTranslate(x, y, z)
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


def init_tex(tex_name, rect_name, a=1, x=0, y=0, z=0, r=1, g=1, b=1):
    glEnable(GL_TEXTURE_2D)
    tex_name.draw_tex()
    DrawRectangle(rect_name, a, x, y, z, r, g, b)
    glDisable(GL_TEXTURE_2D)

# loading textures
clouds_tex = Texture('Textures/clouds.png')
clouds_tex.load()
background_main_tex = Texture('Textures/background_5.png')
background_main_tex.load()
background2_main_tex = Texture('Textures/background_3.png')
background2_main_tex.load()
tank1_tex = Texture('Textures/tank11.png')
tank1_tex.load()
tank2_tex = Texture('Textures/tank112.png')
tank2_tex.load()
turret_tex = Texture('Textures/tanks_turret3.png')
turret_tex.load()
bg_N_tex = Texture('Textures/gui_panel_N.png')
bg_N_tex.load()
bg_D_tex = Texture('Textures/gui_panel_D.png')
bg_D_tex.load()
fire_button_tex = Texture('Textures/fire_button_f.png')
fire_button_tex.load()
move_button_tex = Texture('Textures/button_f.png')
move_button_tex.load()
Angle_button_tex = Texture('Textures/button_f.png')
Angle_button_tex.load()
Power_slider_tex = Texture('Textures/button_f.png')
Power_slider_tex.load()
Weapon_Button_tex = Texture('Textures/Weapong.png')
Weapon_Button_tex.load()

Weapon_type_tex = Texture('Textures/ico_bigshot.png')
Weapon_type_tex.load()
Weapon_0_tex = Texture('Textures/ico_zapper.png')
Weapon_0_tex.load()
Weapon_2_tex = Texture('Textures/ico_threeshot.png')
Weapon_2_tex.load()
Weapon_4_tex = Texture('Textures/ico_scattershot.png')
Weapon_4_tex.load()
baly_projectile_tex = Texture('Textures/Projectiles/baly_projectile.png')
baly_projectile_tex.load()
pocket_tanks = Texture('Textures/tex.png')
pocket_tanks.load()
play_button_r = Texture('Textures/play_button_r.png')
play_button_r.load()
play_button_b = Texture('Textures/play_button.png')
play_button_b.load()
splash_logo_tex = Texture('Textures/pocket_tanks_intro.png')
splash_logo_tex.load()
splash_background_tex = Texture('Textures/splash_background3.png')
splash_background_tex.load()
splash_tank_r_tex = Texture('Textures/tank_splash_r.png')
splash_tank_r_tex.load()
splash_tank_l_tex = Texture('Textures/tank_splash_l.png')
splash_tank_l_tex.load()
background_tex = Texture('Textures/background.png')
background_tex.load()
game_mode2_bg_tex = Texture('Textures/game_mode_2BG.png')
game_mode2_bg_tex.load()
pocket_tanks_intro_tex = Texture('Textures/pocket_tanks_intro.png')
pocket_tanks_intro_tex.load()
earth_day_tex = Texture('Textures/earth_day2.png')
earth_day_tex.load()
earth_night_tex = Texture('Textures/earth_day2.png')
earth_night_tex.load()
#########night_Mode_Buttons########
angle_power_tex = Texture('Textures/Buttons/Night/angle-power-1011-20.png')
angle_power_tex.load()
Fire_tex = Texture('Textures/Buttons/Night/Fire-832-20.png')
Fire_tex.load()
move_tex = Texture('Textures/Buttons/Night/move-622-50.png')
move_tex.load()

############ Game_mode2_buttons ############
Startgame_button_tex = Texture('Textures/Buttons/Startgame-180-177.png')
Startgame_button_tex.load()
Resumegame_button_tex = Texture('Textures/Buttons/ResumeGame-180-177.png')
Resumegame_button_tex.load()
Audio_button_tex = Texture('Textures/Buttons/Audio-842-360.png')
Audio_button_tex.load()
Music_button_tex = Texture('Textures/Buttons/Music-1072-360.png')
Music_button_tex.load()
Settings_button_tex = Texture('Textures/Buttons/Settings-958-360.png')
Settings_button_tex.load()
HTP_button_tex = Texture('Textures/Buttons/HTP-920-250.png')
HTP_button_tex.load()
HE_MODES_button_tex = Texture('Textures/Buttons/HE-MODES_1055-122.png')
HE_MODES_button_tex.load()
Theme_button_tex = Texture('Textures/Buttons/Theme-842-122.png')
Theme_button_tex.load()
Hard_text_tex = Texture('Textures/Buttons/hard-1047-138.png')
Hard_text_tex.load()
Easy_text_tex = Texture('Textures/Buttons/Easy-1047-138.png')
Easy_text_tex.load()
day_text_tex = Texture('Textures/Buttons/Day-888-138.png')
day_text_tex.load()
night_text_tex = Texture('Textures/Buttons/Night-871-138.png')
night_text_tex.load()
Exit_button_tex = Texture('Textures/Buttons/Exit.png')
Exit_button_tex.load()

############ WEAPONS ############

bazooka_tex = Texture('Textures/bazooka2.png')
bazooka_tex.load()
acid_rain_tex = Texture('Textures/clouds.png')
acid_rain_tex.load()
single_shot_tex = Texture('Textures/Projectiles/baly_projectile.png')
single_shot_tex.load()
shot_tex = Texture('Textures/Projectiles/shot.png')
shot_tex.load()
shot2_tex = Texture('Textures/Projectiles/shot-2.png')
shot2_tex.load()
shot3_tex = Texture('Textures/Projectiles/shot-3.png')
shot3_tex.load()


#######Texts Textures ######
player_1_day_tex = Texture('Textures/Texts/player_1_day.png')
player_1_day_tex.load()
player_2_day_tex = Texture('Textures/Texts/player_2_day.png')
player_2_day_tex.load()
player_1_night_tex = Texture('Textures/Texts/player_1_night.png')
player_1_night_tex.load()
player_2_night_tex = Texture('Textures/Texts/player_2_night.png')
player_2_night_tex.load()

night_slider_left_tex = Texture('Textures/night_slider_left_0_284.png')
night_slider_left_tex.load()
night_slider_right_tex = Texture('Textures/night_slider_right_0_284.png')
night_slider_right_tex.load()

day_slider_left_tex = Texture('Textures/day_slider_left_0_284.png')
day_slider_left_tex.load()
day_slider_right_tex = Texture('Textures/day_slider_right_0_284.png')
day_slider_right_tex.load()

weapons_bazooka_tex = Texture('Textures/bazooka_0_574.png')
weapons_bazooka_tex.load()
weapons_single_shot_tex = Texture('Textures/single_shot_0_574.png')
weapons_single_shot_tex.load()
weapons_three_shot_tex = Texture('Textures/Three-shot_0_574.png')
weapons_three_shot_tex.load()
weapons_tommy_gun_tex = Texture('Textures/Tommy Gun_0_574.png')
weapons_tommy_gun_tex.load()
weapons_acid_rain_tex = Texture('Textures/Acid Rain_0_574.png')
weapons_acid_rain_tex.load()
weapons_super_lazer_tex = Texture('Textures/Super Lazer_0_574.png')
weapons_super_lazer_tex.load()
weapons_skipper_tex = Texture('Textures/skipper_0_574.png')
weapons_skipper_tex.load()

weapons_icon_bazooka_tex = Texture('Textures/ico_homingmissile.png')
weapons_icon_bazooka_tex.load()
weapons_icon_single_shot_tex = Texture('Textures/ico_singleshot.png')
weapons_icon_single_shot_tex.load()
weapons_icon_three_shot_tex = Texture('Textures/ico_threeshot.png')
weapons_icon_three_shot_tex.load()
weapons_icon_tommy_gun_tex = Texture('Textures/ico_tommygun.png')
weapons_icon_tommy_gun_tex.load()
weapons_icon_acid_rain_tex = Texture('Textures/ico_acidrain.png')
weapons_icon_acid_rain_tex.load()
weapons_icon_super_lazer_tex = Texture('Textures/ico_laser.png')
weapons_icon_super_lazer_tex.load()
weapons_icon_skipper_tex = Texture('Textures/ico_skipper.png')
weapons_icon_skipper_tex.load()

#####Sub windows######
subwindow_credits_tex =  Texture('Textures/subwindow_credits_1280x720.png')
subwindow_credits_tex.load()
Game_End_subwindow_tex =  Texture('Textures/Subwindows/Game_End_subwindow.png')
Game_End_subwindow_tex.load()
weapons_slider_tex = Texture('Textures/weapons_slider_0_284.png')
weapons_slider_tex.load()