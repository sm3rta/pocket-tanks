from Splash import *
from Variables import *


def game_options_display():
    print("display 2")
    print(Resume)
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    init_tex(game_mode2_bg_tex, game_mode2_bg)
    init_tex(Startgame_button_tex, Startgame_button)
    if credits_sub_menu == 1:
        init_tex(subwindow_credits_tex,subwindow_credits)
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

    glutSwapBuffers()
