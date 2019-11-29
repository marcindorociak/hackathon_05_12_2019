import pyautogui
import time
import numpy as np
import imutils
import cv2
import re
import os
try:
    from PIL import Image
except ImportError:
    import Image

from pytesseract import pytesseract
from collections import OrderedDict

time.sleep(5)
i = 0
old_cur_pos = 0
after_details = False

def advance_contour_filtering(image, option):
    global after_details
    image_copy = np.copy(image)
    image_length = len(image)
    if option != "detail":
        for i, values in enumerate(image):
            for j, (x, y, z) in enumerate(values):
                j2 = j
                if option == '':
                    if z == 160 and y == 160 and x == 160 and j + 3 < len(values):
                        if image_copy[i][j][0] != image_copy[i][j + 3][0]:
                            image_copy[i][j] = image_copy[i][j + 3]
                        elif i + 4 < image_length:
                            image_copy[i][j] = image_copy[i + 4][j2]      
                 
                if (after_details == False and option == 'group') or option == 'empty':
                    if i < 20 and j > 100 and j + 5 < len(values):
                        j2 = j + 5
                        if j < 107 and j > 101:
                            image_copy[i][j] = [255, 255, 255]
                        image_copy[i][j2] = image[i][j]

                if option == 'page':
                    if z > 50 and z < 137 and y > 100 and y < 171 and x > 70 and x < 215:
                         image_copy[i][j2] = [255, 255, 255]
                    # else:
                    #      image_copy[i][j2] = [0, 0, 0]
                    # if i < 20 and j > 77 and j + 5 < len(values):
                    #     j2 = j + 5
                    #     if j < 85 and j > 78:
                    #         image_copy[i][j] = [255, 255, 255]
                    #     image_copy[i][j2] = image[i][j]

                if option == 'footer1':
                    if i < 20 and j > 95 and j + 10 < len(values):
                        j2 = j + 10
                        if j < 106 and j > 96:
                            image_copy[i][j] = image_copy[20][120]
                        image_copy[i][j2] = image[i][j]

                if option == 'footer2':
                    if i < 20 and j == 106:
                        image_copy[i][j] = image_copy[20][120]

                if option == "footer3":
                    if z > 50 and z < 137 and y > 100 and y < 171 and x > 70 and x < 215:
                         image_copy[i][j2] = [255, 255, 255]
                    else:
                         image_copy[i][j2] = [0, 0, 0]
    if option == 'detail':
        image_copy = image_copy[0:30, 10:70]
    if option == 'page':
        image_copy = image_copy[0:30, 10:100]

            # if i < 20 and j > 94  and j < 101 and j + 5 < len(values):
            #     j2 = j + 5
            #     if j < 101 and j > 95:
            #         image_copy[i][j] = [255, 255, 255]
            #     image_copy[i][j2] = image[i][j]
           

    return image_copy

def save_and_ocr(myScreenshot, part):
    global after_details
    global i
    myScreenshot = change_colors(myScreenshot)
    if part == "0":
        myScreenshot = advance_contour_filtering(myScreenshot, "")
    cv2.imwrite('filename' + part + '_' + str(i) + '.png', myScreenshot)
    if part == "0":
        datails_string = pytesseract.image_to_string(Image.open('filename' + part + '_' + str(i) + '.png'),
                                                     config='-c load_system_dawg=false load_freq_dawg=false', lang="fra+eng").lower()
        if any(x in datails_string for x in ["detail", "detal", "detai"]):
            after_details = True
            myScreenshot = advance_contour_filtering(myScreenshot, "detail")
            cv2.imwrite('filename' + part + '_' +
                        str(i) + '.png', myScreenshot)
        if any(x in datails_string for x in ["page"]):
            if after_details == False:
                myScreenshot = advance_contour_filtering(myScreenshot, "group")
            else:
                myScreenshot = advance_contour_filtering(myScreenshot, "page")
            cv2.imwrite('filename' + part + '_' + str(i) + '.png', myScreenshot)

        if after_details == False and any(x in datails_string for x in ["group"]):
            if datails_string.split('\n', 1)[0].endswith(':'):
                myScreenshot = advance_contour_filtering(myScreenshot, "group")
                cv2.imwrite('filename' + part + '_' + str(i) + '.png', myScreenshot)
        if datails_string == "":
            myScreenshot = advance_contour_filtering(myScreenshot, "empty")
            cv2.imwrite('filename' + part + '_' +
                        str(i) + '.png', myScreenshot)
            datails_string = pytesseract.image_to_string(Image.open('filename' + part + '_' + str(i) + '.png'),
                                                         config='-c load_system_dawg=false load_freq_dawg=false', lang="fra+eng").lower()
            if datails_string == "" and i > 1:
                while not pyautogui.locateOnScreen('break_line.png', region=(230, 197, 21, 100)):
                    pyautogui.press('up')
                top3 = pyautogui.locateOnScreen('break_line.png', region=(230, 197, 21, 100))[1]
                myScreenshot = pyautogui.screenshot(region=(5, top3, 145, 50))
                myScreenshot = cv2.cvtColor(np.array(myScreenshot), cv2.COLOR_RGB2BGR)
                save_and_ocr(myScreenshot, part)
                while not pyautogui.locateOnScreen('break_line.png', region=(230, 900, 21, 100)):
                    pyautogui.press('down')
                return
            
        if after_details and check_if_last_is_letter(datails_string) == False:
            myScreenshot = advance_contour_filtering(myScreenshot, "footer1")
            cv2.imwrite('filename' + part + '_' + str(i) + '.png', myScreenshot)
            datails_string = pytesseract.image_to_string(Image.open('filename' + part + '_' + str(
                i) + '.png'), config='-c load_system_dawg=false load_freq_dawg=false', lang="fra+eng").lower()
            if check_if_last_is_letter(datails_string) == False:
                myScreenshot = advance_contour_filtering(myScreenshot, "footer2")
                cv2.imwrite('filename' + part + '_' +
                            str(i) + '.png', myScreenshot)
                datails_string = pytesseract.image_to_string(Image.open('filename' + part + '_' + str(i) + '.png'), 
                                config='-c load_system_dawg=false load_freq_dawg=false', lang="fra+eng").lower()
                if check_if_last_is_letter(datails_string) == False:
                    myScreenshot = advance_contour_filtering(myScreenshot, "footer3")
                    cv2.imwrite('filename' + part + '_' + str(i) + '.png', myScreenshot)
                
    if part == "2":
        pytesseract.run_tesseract(
            'filename' + part + '_' + str(i) + '.png', 'filename' + part + '_' + str(i), lang="fra+eng", extension='hocr', 
            config='-c load_system_dawg=false load_freq_dawg=false')
        files_were_deleted = False
    else:
        pytesseract.run_tesseract(
            'filename' + part + '_' + str(i) + '.png', 'filename' + part + '_' + str(i), lang="fra+eng", extension='',
            config='-c load_system_dawg=false load_freq_dawg=false')
        files_were_deleted = clean_file('filename' + part + '_' + str(i) + '.txt')
    if not files_were_deleted:
        png_index = i
    else:
        png_index = i + 1
    
    os.remove('filename' + part + '_' + str(png_index) + '.png')
    

def clean_file(file_name):
    global i
    txt_file = open(file_name, 'r', encoding="utf8")
    txt_datas = txt_file.readlines()
    for j, txt_data in enumerate(txt_datas):
        if j == 0:
            txt_data = txt_data.lower()
        to_replace = OrderedDict(
            [("|", ""), (",", "_"), ("detals", "details"), ("detais", "details"), ("‘", ""), 
            ("É", "E"), ("detail ", "details ")])
        txt_data = replace_all(txt_data, to_replace)
        txt_data = re.sub(' +', ' ', txt_data)
      #  txt_data = re.sub(r"^\s+|\s+$", "", txt_data)
        txt_datas[j] = txt_data
    
    test_data = re.sub(r"^\s+|\s+$", "", txt_datas[0])
    to_replace = OrderedDict(
        [(".", ""), ("ÿ", "g"), ("9", "g"), (":", ""), ("à", "q"), ("¢", "c"), ("#", "")])
    test_data = replace_all(test_data, to_replace)
    txt_datas[0] = test_data[: -1] + " " + test_data[-1:]

    to_replace = OrderedDict(
        [("foote r", "footer"), ("heade r", "header"), ("detail s", "details")])
    txt_datas[0] = replace_all(txt_datas[0], to_replace)

    txt_datas[0] = re.sub(' +', ' ', txt_datas[0])

    output_table = fill_when_end_is_not_recognized_by_ocr(txt_datas[0], i)
    txt_datas[0] = output_table[0] + "\n"
    if output_table[1]:
        txt_file.close()
        os.remove('filename0_' + str(i) + '.txt')
        i -= 1
        return True
    else:
        txt_file = open(file_name, 'w', encoding="utf8")
        txt_file.writelines(txt_datas)
        txt_file.close()
        return False

def fill_when_end_is_not_recognized_by_ocr(file_text, i):
    rename_to_previous = False
    if i > 1:
        txt_file = open('filename0_' + str(i-1) + '.txt', 'r', encoding="utf8")
        txt_data = txt_file.readline()
        txt_data = re.sub(r"^\s+|\s+$", "", txt_data)
        if txt_data == file_text:
            txt_file.close()
            rename_to_previous = True
    


        # file_text_split = file_text.split(" ")
        # if len(file_text_split) == 1 and i > 2:
        #      txt_file = open('filename0_' + str(i-1) + '.txt', 'r', encoding="utf8")
        #      txt_datas = txt_file.readline()
            

    return [file_text, rename_to_previous]

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text
def check_if_last_is_letter(text):
    text = text.split('\n', 1)[0]
    if text.endswith(':'):
        text = text[:-1]
    if text[-1:].isalpha():
        return True
    return False

def change_colors(img):
    img[np.where((img == [150, 150, 150]).all(axis=2))] = [0, 0, 0]
    img[np.where((img == [105, 132, 0]).all(axis=2))]   = [0, 0, 0]
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


def scan_action():
    global after_details
    global i
    global old_cur_pos
    
    l = 0
    height2 = 0
    top2 = 0
    cur_possition = pyautogui.locateOnScreen('break_line.png', region=(230, 900, 21, 100))
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
            myScreenshot = cv2.cvtColor(
                np.array(myScreenshot), cv2.COLOR_RGB2BGR)
            save_and_ocr(myScreenshot, "0")

            myScreenshot1 = pyautogui.screenshot(
                region=(180, top2, 1555, height2))
            myScreenshot1 = cv2.cvtColor(
                np.array(myScreenshot1), cv2.COLOR_RGB2BGR)

        scroll_horizontally("right")
        if top2 > 0:
            myScreenshot2 = pyautogui.screenshot(
                region=(181, top2, 1555, height2))
            myScreenshot2 = cv2.cvtColor(
                np.array(myScreenshot2), cv2.COLOR_RGB2BGR)
            myScreenshot = np.concatenate(
                (myScreenshot1, myScreenshot2), axis=1)
            save_and_ocr(myScreenshot, "2")
            i += 1

        myScreenshot = pyautogui.screenshot(region=(5, top, 145, 50))
        myScreenshot = cv2.cvtColor(
            np.array(myScreenshot), cv2.COLOR_RGB2BGR)
        save_and_ocr(myScreenshot, "0")

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
        save_and_ocr(myScreenshot, "2")

while not pyautogui.locateOnScreen('bottom_end.png', region=(1700, 900, 60, 100)):
    scan_action()
    pyautogui.press('down')
scan_action()
