'''
CST 205
Face and feature detection
Class and functions that can be used to detect
a face, smile, mouth, and eyes.
Authors: Scott Grether, Dustin Grady, Michael Royal
10/14/2016
GitHub: https://github.com/sgrether/Project-2
'''
import numpy as np
import cv2
import sys

'''
Class for main face in image
Detects nearest face and provides variables that helps with
detection of other features.
Written by: Scott Grether
'''
class Face():
    def __init__(self, image):
        faceCascade = cv2.CascadeClassifier("haarscascade_frontalface_default.xml")
        self.img = cv2.imread(image)

        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        #Get list of all faces in image
        faces = faceCascade.detectMultiScale(
            self.gray,
            scaleFactor = 1.10,
            minNeighbors = 8,
            minSize = (55,55),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        self.face = closestFace(faces) #get closest face
    #Return class variables for use in other functions
    def getGray(self):
        return self.gray
    def getFace(self):
        return self.face
    def getImage(self):
        return self.img

'''
Helper function for face class.
Written by: Scott Grether
'''
def closestFace(faces):
    #Error checking
    if(len(faces) < 1):
        print('No face detected.')
        sys.exit()
    biggestRect = faces[0]
    #Loop through all faces detected and keep the largest
    for i in range(len(faces)):
        rect = faces[i]
        #Check for biggest face
        if (rect[2] > biggestRect[2] and rect[3] > biggestRect[3]):
            biggestRect = rect
    return biggestRect
'''
Helper function for detecting other features.
Written by: Scott Grether
'''
def get_roi_gray(face):
    return face.getGray()[face.getFace()[1]:face.getFace()[1]+face.getFace()[3], face.getFace()[0]:face.getFace()[0]+face.getFace()[2]]

'''
Helper function for drawing rectangles around detected features.
Written by: Scott Grether
'''
def get_roi_color(face):
    temp = face.getFace()
    tempImg = face.getImage()
    return tempImg[temp[1]:temp[1]+temp[3], temp[0]:temp[0]+temp[2]]

'''
Detect a smile in the given face.
Adapted from code written by: Dustin Grady
'''
def findSmile(face):
    smileCascade = cv2.CascadeClassifier("haarcascade_smile.xml")
    smiles = smileCascade.detectMultiScale(
    get_roi_gray(face),
    scaleFactor = 2.25,
    minNeighbors = 22,
    minSize = (25, 25),
    flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    #Check if any smiles were found
    if (len(smiles) >= 1):
        return True
    else:
        return False
