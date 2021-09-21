import pyautogui as pg
import keyboard as kb
from time import sleep



def click_only(pos1x, pos1y, sleep_timer = 1, clicks = 1):
    pg.click(x = pos1x, y = pos1y, clicks = clicks, interval = 0.08)
    sleep(sleep_timer)

def right_and_left_click(pos1x, pos1y, pos2x, pos2y, sleep_timer1 = 1, sleep_timer2 = 1):
    pg.click(x = pos1x, y = pos1y, button = 'right')
    sleep(sleep_timer1)
    pg.click(x = pos2x, y = pos2y)
    sleep(sleep_timer2)

def click_and_drag(pos1x, pos1y, pos2x, pos2y, sleep_timer = 1):
    pg.moveTo(x = pos1x, y = pos1y)
    sleep(0.1)
    pg.dragTo(x = pos2x, y = pos2y, duration = 0.25)
    sleep(sleep_timer)

def write_only(text = '', sleep_timer = 1, select_text = 0):
    if select_text != 0:
        click_only(None, None, 0.1, 3)
    kb.write(text)
    sleep(sleep_timer)

def write_and_execute(text = '', sleep_timer1 = 1, sleep_timer2 = 1, select_text = 0):
    write_only(text, sleep_timer1, select_text)
    kb.press_and_release('enter')
    sleep(sleep_timer2)

def hover_only(pos1x, pos1y, sleep_timer = 1, duration = 1):
    pg.moveTo(x = pos1x, y = pos1y, duration = duration)
    sleep(sleep_timer)

def press_and_release(command, sleep_timer = 1, number_of_presses = 1):
    for i in range(number_of_presses):
        kb.press_and_release(hotkey = command)
        sleep(sleep_timer)

def scroll(pixels = 5000, scroll_movement = 'down'):
    if scroll_movement == 'up':
        pixels = abs(pixels)
    else:
        pixels = -abs(pixels)
    pg.scroll(pixels)
