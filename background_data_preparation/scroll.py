import pyautogui
import time
import numpy as np
import imutils
import cv2

time.sleep(5)
i = 0
myScreenshot = pyautogui.screenshot(region=(0, 197, 180, 50))
myScreenshot.save(r'filename0_' + str(i) + '.png')
myScreenshot = pyautogui.screenshot(region=(190, 197, 1540, 797))
myScreenshot.save(r'filename1_' + str(i) + '.png')
old_cur_pos = 0

while i < 20:
        l = 0
    # while l < 24:
    #     l += 1
    #     if l == 24:
    #         i += 1
    #         myScreenshot = pyautogui.screenshot(region=(0, 197, 180, 50))
    #         myScreenshot.save(r'filename0_' + str(i) + '.png')
    #         myScreenshot = pyautogui.screenshot(region=(190, 197, 1540, 797))
    #         myScreenshot.save(r'filename1_' + str(i) + '.png')
    #         break
        cur_possition = pyautogui.locateOnScreen('break_line.png', region=(230, 800,21, 210))
        if cur_possition:
            print(cur_possition)
            cur_possition = list(pyautogui.locateAllOnScreen('break_line.png', region=(230, 197, 21, 797)))
            list_length = len(cur_possition)
            print(cur_possition)
            if len(cur_possition) == 1:
                top = 197
                height = cur_possition[0][1] - top
            elif len(cur_possition) == 2:
                top = cur_possition[0][1]
                height = cur_possition[1][1] - top
            else:
                top = cur_possition[list_length-2][1]
                height = cur_possition[list_length-1][1] - top
            print (top)
            print (height)
            i += 1
            myScreenshot = pyautogui.screenshot(region=(0, top, 180, 50))
            myScreenshot = cv2.cvtColor(np.array(myScreenshot), cv2.COLOR_RGB2BGR)
            cv2.imwrite('filename0_' + str(i) + '.png', myScreenshot)

            myScreenshot = pyautogui.screenshot(region=(190, top, 1540, height))
            myScreenshot = cv2.cvtColor(np.array(myScreenshot), cv2.COLOR_RGB2BGR)
            cv2.imwrite('filename1_' + str(i) + '.png', myScreenshot)
            pyautogui.scroll(-100)
            pyautogui.scroll(-100)
            pyautogui.scroll(-100)
            pyautogui.scroll(-100)
            pyautogui.scroll(-100)
            pyautogui.scroll(-100)

        pyautogui.scroll(-100)



