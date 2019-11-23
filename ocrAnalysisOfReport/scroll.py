import pyautogui
import time
import numpy as np
import imutils
import cv2

from pytesseract import pytesseract

time.sleep(5)
i = 0
old_cur_pos = 0

def advance_contour_filtering(image):
    for i, values in enumerate(image):
        for j, (x, y, z) in enumerate(values):
            if y > 132 and y < 171:
                print(y)
            if x > 94 and x < 137 and y > 132 and y < 171 and z > 182 and z < 215:
                image[i][j] = [255, 255, 255]
    return image

def save_and_ocr(myScreenshot, i, part):
    myScreenshot = change_colors(myScreenshot)
    if part == "0":
        myScreenshot = advance_contour_filtering(myScreenshot)
    cv2.imwrite('filename' + part + '_' + str(i) + '.png', myScreenshot)
    pytesseract.run_tesseract(
        'filename' + part + '_' + str(i) + '.png', 'filename' + part + '_' + str(i), lang=None, extension='hocr', config='-c load_system_dawg=false load_freq_dawg=false')

def change_colors(img):
    img[np.where((img == [150, 150, 150]).all(axis=2))] = [0, 0, 0]
    img[np.where((img == [109, 109, 109]).all(axis=2))] = [255, 255, 255]

    return img
def scroll_horizontally (direction):
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)
    pyautogui.press(direction)

while not pyautogui.locateOnScreen('bottom_end.png', region=(1700, 900, 60, 100)):
        l = 0
        height2 = 0
        top2 = 0
        cur_possition = pyautogui.locateOnScreen('break_line.png', region=(230, 900,21, 100))
        if cur_possition:
            cur_possition = list(pyautogui.locateAllOnScreen('break_line.png', region=(230, 197, 21, 797)))
            list_length = len(cur_possition)
            if len(cur_possition) == 1:
                top = 197
                height = cur_possition[0][1] - top
            elif len(cur_possition) == 2:
                top = cur_possition[0][1]
                height = cur_possition[1][1] - top
            else:
                top = cur_possition[list_length-2][1]
                height = cur_possition[list_length-1][1] - top
                if cur_possition[list_length-2][1] > 900:
                    top2 = cur_possition[list_length-3][1]
                    height2 = cur_possition[list_length-2][1] - top2

            i += 1

            if top2 > 0:
                myScreenshot = pyautogui.screenshot(region=(5, top2, 145, 50))
                myScreenshot = cv2.cvtColor(np.array(myScreenshot), cv2.COLOR_RGB2BGR)
                save_and_ocr(myScreenshot, i , "0")

                myScreenshot1 = pyautogui.screenshot(region=(180, top2, 1555, height2))
                myScreenshot1 = cv2.cvtColor(np.array(myScreenshot1), cv2.COLOR_RGB2BGR)

            scroll_horizontally("right")
            if top2 > 0:
                myScreenshot2 = pyautogui.screenshot(
                    region=(181, top2, 1555, height2))
                myScreenshot2 = cv2.cvtColor(np.array(myScreenshot2), cv2.COLOR_RGB2BGR)
                myScreenshot = np.concatenate(
                    (myScreenshot1, myScreenshot2), axis=1)
                save_and_ocr(myScreenshot, i, "2")
                i += 1

            myScreenshot = pyautogui.screenshot(region=(5, top, 145, 50))
            myScreenshot = cv2.cvtColor(
                np.array(myScreenshot), cv2.COLOR_RGB2BGR)
            save_and_ocr(myScreenshot, i, "0")

            myScreenshot2 = pyautogui.screenshot(
                region=(181, top, 1555, height))
            myScreenshot2 = cv2.cvtColor(
                np.array(myScreenshot2), cv2.COLOR_RGB2BGR)

            scroll_horizontally("left")

            myScreenshot1 = pyautogui.screenshot(
                region=(180, top, 1555, height))
            myScreenshot1 = cv2.cvtColor(
                np.array(myScreenshot1), cv2.COLOR_RGB2BGR)
            myScreenshot = np.concatenate(
                (myScreenshot1, myScreenshot2), axis=1)
            save_and_ocr(myScreenshot, i, "2")
            
        pyautogui.press('down')



