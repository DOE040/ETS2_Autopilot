import cv2, pyautogui
import numpy as np
from PIL import Image, ImageEnhance, ImageStat
import time
import threading
import vgamepad as vg

gamepad = vg.VX360Gamepad()
# press a button to wake the device up
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()

greenleft = 0
vvdright = 0

# Steering
def steering():
    while True:
        global greenleft, vvdright
        if greenleft > vvdright:  #Steer left
            gamepad.left_trigger(value=0)
            gamepad.right_trigger(value=int((greenleft - vvdright) / 10))
            gamepad.update()
            #print("steer left")
        elif vvdright > greenleft:  #Steer right
            gamepad.left_trigger(value=int((vvdright - greenleft) / 10))
            gamepad.right_trigger(value=0)
            gamepad.update()
            #print("steer right")

mofpunt = (960, 720)

# define white color range
minimum = np.array([0, 0, 230])
maximum = np.array([360, 10, 255])

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 5  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 5  # minimum number of pixels making up a line
max_line_gap = 50  # maximum gap in pixels between connectable line segments

kernel_size = 9

low_threshold = 50
high_threshold = 150

t = threading.Thread(target=steering, daemon=True)
t.start()

while True:
    t1 = time.perf_counter()
    #im = Image.open("img.jpg")
    im = pyautogui.screenshot()
    cimage = im.crop((760, 620, 1160, 1020))
    stat = ImageStat.Stat(cimage)
    print(stat.mean[0])
    #image brightness & contrast enhancer
    im = ImageEnhance.Brightness(im).enhance(0.005*(150/stat.mean[0]))
    im = ImageEnhance.Contrast(im).enhance(500)
    image = np.array(im)

    # Detect distance from point to road mark
    greenstop = False
    vvdstop = False
    groenlinks = greenleft
    vvdrechts = vvdright
    greenleft = 0
    vvdright = 0
    while True:
        if not greenstop: greenleft += 2
        if not vvdstop: vvdright += 2
        if greenstop and vvdstop: break
        try:
            if np.any(image[mofpunt[1], mofpunt[0]-greenleft] != 0): greenstop = True
            if np.any(image[mofpunt[1], mofpunt[0] + vvdright] != 0): vvdstop = True
        except IndexError:
            vvdright = greenleft
            break
    if greenleft > 500: greenleft = groenlinks
    if vvdright > 500: vvdright = vvdrechts
    cv2.line(image, mofpunt, (mofpunt[0]-greenleft, mofpunt[1]), (0, 0, 255), 5)
    cv2.line(image, mofpunt, (mofpunt[0]+vvdright, mofpunt[1]), (0, 255, 0), 5)

    cv2.imshow("Color Detected", image)
    t2 = time.perf_counter()
    print(t2 - t1)
    cv2.waitKey(2)
