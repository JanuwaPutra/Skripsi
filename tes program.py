import cv2
import numpy as np

jenis           = ['busuk','fresh']
jum_per_data    = 20

file_name = "../PROGRAM/uji/cropsenafti.png"

src = cv2.imread(file_name, 1)
src     = cv2.resize(src, (640, 640))
tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_,mask = cv2.threshold(tmp,140,255,cv2.THRESH_BINARY_INV)
mask   = cv2.dilate(mask.copy(),None,iterations=20)
mask   = cv2.erode(mask.copy(),None,iterations=25)
b, g, r = cv2.split(src)
rgba = [b,g,r, mask]
dst = cv2.merge(rgba,4)

contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
selected    = max(contours,key=cv2.contourArea)
x,y,w,h     = cv2.boundingRect(selected)
cropped     = dst[y:y+h,x:x+w]

gray        = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)


# RGB-HSV
hsv_image   = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
H = hsv_image[:,:,0]
S = hsv_image[:,:,1]
V = hsv_image[:,:,2]

        
mH = np.mean(H)
S = np.mean(S)
V = np.mean(V)


cv2.imshow('Image Dominant Color', mask)
cv2.waitKey(0)

cv2.imwrite("hasilgambartes/""ok.jpg", mask)     