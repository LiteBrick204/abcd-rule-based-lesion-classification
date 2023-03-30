#!/usr/bin/env python
import cv2
import numpy as np

#Reading the image
def getABCDValue(name):
    img=cv2.imread(name)
    #Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #Initialization required variables
    a,b,c,d = 0,0,0,0

    #Find the contours in the image
    contours, _ = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Loop through the contours
    for contour in contours:
        # Calculate the perimeter of the contour
        perimeter = cv2.arcLength(contour, True)

        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Calculate the circularity of the contour
        circularity = (4 * np.pi * area) / perimeter**2

        # Calculate the compactness of the contour
        compactness = (area**2) / perimeter

        # Calculate the convexity of the contour
        convexity = cv2.isContourConvex(contour)

        # Increment variables for ABCD rule based on values calculated above
        if circularity >= 0.6:
            a +=(circularity)
        if compactness >= 50:
            b += (100/compactness)
        if convexity == False:
            c += (1)
        if perimeter >= 300:
            d += (perimeter/100)

    #Calculate the percentage of contours that meet each criterion
    a/=len(contours)
    c/=len(contours)
    d/=len(contours)
    d = d*0.01
    a = "{:.2f}".format(a)
    b = "{:.0f}".format(b)
    c = "{:.2f}".format(c)
    d = "{:.2f}".format(d)
    return [a,b,c,d]
