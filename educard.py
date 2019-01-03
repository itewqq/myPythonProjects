# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 09:48:54 2018

@author: qushipei
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image

debug=1
lot=170
imgPath="testPic3.jpg"

def stechCr(img):
    dst = cv2.equalizeHist(img)
    cv2.imshow('dst',dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return dst


def makepic(Img):
    Img=stechCr(Img)
    ret, img = cv2.threshold(Img, lot, 255, cv2.THRESH_BINARY)
    image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    res=contours[0]
    carea=cv2.contourArea(res)
    tmpImg=Img
    cv2.drawContours(tmpImg,contours,-1,(0,0,255),3)
    cv2.imwrite('contours.png',tmpImg)
    for i in range(len(contours)):
        cnt=contours[i]
        narea=cv2.contourArea(cnt)
        if carea < narea :
            carea=narea
            res=cnt
    rect = cv2.minAreaRect(res)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    h = abs(box[0][1] - box[2][1])
    
    w = abs(box[0][0] - box[2][0])
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    y1 = min(Ys)
    r1=cv2.resize(Img[y1:y1 + h, x1:x1 + w],(560*2,340*2),interpolation=cv2.INTER_CUBIC)
    r2=cv2.resize(img[y1:y1 + h, x1:x1 + w],(560*2,340*2),interpolation=cv2.INTER_CUBIC)
    if debug:
        cv2.imshow('ROI',Img[y1:y1 + h, x1:x1 + w])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return r1,r2

def prepare(gray):
    ret, binary = cv2.threshold(gray, lot, 255, cv2.THRESH_BINARY_INV)
    #膨胀操作
    opening=binary
    ele = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 17))
    dilation = cv2.dilate(opening, ele, iterations=1)
    cv2.imwrite("BI_img.png", binary)
    cv2.imwrite("AfterDilate.png", dilation)
    if debug :
        cv2.imshow("BI_img", binary)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow("AfterDilate", dilation)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return dilation


def findTextRegion(img):
    region = []
    # 查找轮廓
    image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)
        # 面积过大过小的都去掉掉
        if (area < 4*1500 or area >2*15000):#调参使得适合一卡通
            continue
        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        #函数 cv2.minAreaRect() 返回一个Box2D结构 rect：（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）。
#        if debug:
#            print("rect is: ", rect)
        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        # 筛选矩形
        if (height > width * 1.2):
            continue

        if (height * 15 < width):
            continue
        #if (width > img.shape[1] / 2 and height > img.shape[0] / 20):
        region.append(box)
        
    return region


def detect(img):
    gray = cv2.fastNlMeansDenoisingColored(img, None, 10, 3, 3, 3)
    gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
    img,gray=makepic(gray)
    cv2.imshow('tmp1',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('tmp2',gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if debug:
        cv2.imwrite("gray.png", gray)
    #二值化和膨胀变换
    dilation = prepare(gray)
    if debug:
        cv2.imwrite('dilation.png',dilation)
    #文字区域
    region = findTextRegion(dilation)
    #画出文本框
    idImg=[]
    i=0
    for box in region:
        h = abs(box[0][1] - box[2][1])
        w = abs(box[0][0] - box[2][0])
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        y1 = min(Ys)
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
        if(img[y1:y1 + h, x1:x1 + w].size != 0):
            idImg.append(gray[y1:y1 + h, x1:x1 + w])
            cv2.imwrite("idImg"+str(i)+".png", idImg[i])
            cv2.imwrite("contours"+str(i)+".png", img)
        i=i+1
    return idImg




def ocrIdCard(imgPath):
    img = cv2.imread(imgPath)
    infoDict={"学号":"",
              "姓名":"",
              "学院":"",
              "班级":""
            }
    print('start...\n')
    idImgs = detect(img)
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
    tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
    i=1
    for idImg in idImgs:
        #print(i)
        cv2.imshow('temp'+str(i),idImg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        image = Image.fromarray(idImg)
        result = pytesseract.image_to_string(image, lang='chi_sim',config=tessdata_dir_config,)
        result=result.replace(' ','')
        if(len(result)!=0):
            flag=1
            for a in result:
                if (a<='z' and a>='a') or (a<='Z' and a>='A'):
                    flag=0
                    break
            if flag:
                if len(result) == 11:
                    infoDict["学号"]=result
                elif len(result) == 7:
                    infoDict["班级"]=result
                elif result[-2:]=="学院":
                    infoDict["学院"]=result
                else:
                    infoDict["姓名"]=result
        i+=1
    return infoDict


if __name__=="__main__":
    print("kaishi")
    ans=ocrIdCard(imgPath)
    print(ans)




