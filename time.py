""" # adds image processing capabilities
from PIL import Image, ImageEnhance
import pytesseract

# assigning an image from the source path

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = Image.open("media/image3.jpg")# converts the image to result and saves it into result variable

enhancer1 = ImageEnhance.Sharpness(img)
enhancer2 = ImageEnhance.Contrast(img)

edit = enhancer1.enhance(20.0)
edit = enhancer2.enhance(1.5)

result = pytesseract.image_to_string(edit)

print(result) """

# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
   
# path  
#path = r'C:\Users\exces\Desktop\11111111.jpg'
   
# Reading an image in default mode 
src = cv2.imread(path) 
   
window_name = 'Image'
  

def gray(img):
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

# blur
def blur(img) :
    img_blur = cv2.GaussianBlur(img,(5,5),0)  
    return img_blur

# threshold
def threshold(img):
    #pixels with value below 100 are turned black (0) and those with higher value are turned white (255)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]    
    return img

def enhance(img):
    img = gray(img)
    img = blur(img)
    img = threshold(img)
    cv2.imwrite(r"media/new.png", img)

new = enhance(src)
contours = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

print(contours)
""" for cnt in contours: 
    x, y, w, h = cv2.boundingRect(cnt) 

    # Drawing a rectangle on copied image 
    rect = cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 255, 255), 2) 
    
    cv2.imshow('cnt',rect)
    cv2.waitKey()

    # Cropping the text block for giving input to OCR 
    cropped = orig[y:y + h, x:x + w] 

    # Apply OCR on the cropped image 
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(cropped, config=config) 

    print(text)

 """

# Displaying the image  
""" cv2.imshow(window_name, image)
cv2.waitKey(0)
cv2.destroyAllWindows() """
