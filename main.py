from queue import Empty
import pytesseract
import cv2 as cv
import wx
from glob import glob
import sys
import re
import os
from skewd import rotated
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def skew(img_read):
    # Scale reduce
    scale_percent = 10 
    width = int(img_read.shape[1] * scale_percent / 100)
    height = int(img_read.shape[0] * scale_percent / 100)
    dim = (width, height)
    img_temp = cv.resize(img_read, dim, interpolation=cv.INTER_AREA)
    img_skewed, h_ri, h_rf, v_ri, v_rf = rotated(img_temp, img_read)
    img_skewed = img_skewed[h_ri:h_rf, v_ri:v_rf]

    return img_skewed


def rotate(img_skd):
    # Scale reduce
    scale_percent = 90 
    width = int(img_skd.shape[1] * scale_percent / 100)
    height = int(img_skd.shape[0] * scale_percent / 100)
    dim = (width, height)
    image_reduced = cv.resize(img_skd, dim, interpolation=cv.INTER_AREA)
    
    # Orientation finder
    osd = pytesseract.image_to_osd(image_reduced)
    angle = int(re.search('(?<=Rotate: )\d+', osd).group(0))
    if angle == 0:
        pass
    elif angle == 90:
        img_skd = cv.rotate(img_skd, cv.ROTATE_90_CLOCKWISE)
        img_skd = skew(img_skd)
    elif angle == 180:
        img_skd = cv.rotate(img_skd, cv.ROTATE_180)
    elif angle == 270:
        img_skd = cv.rotate(img_skd, cv.ROTATE_90_COUNTERCLOCKWISE)
        img_skd = skew(img_skd)    

    return img_skd


def get_path():
    app = wx.App()
    img_dir = ""
    dialog = wx.DirDialog(None, "[JPG] Select a folder:",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        img_dir = (dialog.GetPath() + "/")
    else:
        print("No folder selected.")
        sys.exit()
    dialog.Destroy()
    return img_dir


def main():
    dir_path = get_path()
    raw_img_list = glob(dir_path + "/*.jpg")
    for img_path in raw_img_list:
        img_name = os.path.basename(img_path)
        img_size = os.path.getsize(img_path)    
        if 100 < img_size:
            img_read = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
            if img_read is None:
                print("Invalid image:", img_name)
            else:
                img_skewed = skew(img_read)
                img_rotated = rotate(img_skewed)
                # DEBUG                
                print(img_name)
                cv.namedWindow("img_original", cv.WINDOW_NORMAL)
                cv.namedWindow("img_skewed_rotated", cv.WINDOW_NORMAL)
                cv.imshow("img_original", img_read)
                cv.imshow("img_skewed_rotated", img_rotated)
                cv.waitKey()
                cv.destroyAllWindows()
        else:
            print("Invalid image:", img_name)


if __name__ == '__main__':
    main()
