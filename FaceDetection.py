import numpy as np
import cv2

#class for main face in image
class detectFace():
    def __init__(self, image):
        faceCascade = cv2.CascadeClassifier("haarscascade_frontalface_default.xml")
        self.img = cv2.imread(image)

        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            self.gray,
            scaleFactor = 1.3,
            minNeighbors = 5,
            minSize = (30,30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        self.face = closestFace(faces) #get closest face

    def getGray(self):
        return self.gray
    def getFace(self):
        return self.face
    def getImage(self):
        return self.img

def closestFace(faces):
    biggestRect = faces[0]
    for i in range(len(faces)):
        rect = faces[i]
        #Check for biggest face
        if (rect[2] > biggestRect[2] and rect[3] > biggestRect[3]):
            biggestRect = rect
    return biggestRect

def get_roi_gray(face):
    return face.getGray()[face.getFace()[1]:face.getFace()[1]+face.getFace()[3], face.getFace()[0]:face.getFace()[0]+face.getFace()[2]]

def get_roi_color(face):
    temp = face.getFace()
    tempIm = face.getImage()
    return tempIm[temp[1]:temp[1]+temp[3], temp[0]:temp[0]+temp[2]]

#Filter through detected "mouths" for the actual mouth
def filterMouth(face):
    mouthCascade = cv2.CascadeClassifier("Mouth.xml")
    mouths = mouthCascade.detectMultiScale(get_roi_gray(face))
    filteredMouth = mouths[0]
    for mouth in mouths:
        if (mouth[1] > filteredMouth[1]):
            filteredMouth = mouth
    return filteredMouth

#Filter through detected "eyes" for the left eye
def filterLeftEye(face):
    leftEyeCascade = cv2.CascadeClassifier("EyeL.xml")
    leftEye = leftEyeCascade.detectMultiScale(get_roi_gray(face))
    filteredLeftEye = leftEye[0]
    for eye in leftEye:
        if (eye[0] < filteredLeftEye[0]):
            filteredLeftEye = eye
    return filteredLeftEye

#Filter through detected "eyes" for the right eye
def filterRightEye(face):
    rightEyeCascade = cv2.CascadeClassifier("EyeR.xml")
    rightEye = rightEyeCascade.detectMultiScale(get_roi_gray(face))
    filteredRightEye = rightEye[0]
    for eye in rightEye:
        if (eye[0] > filteredRightEye[0]):
            filteredRightEye = eye
    return filteredRightEye


#Below code is for testing purposes
face = detectFace('face2.jpg')
mouth = filterMouth(face)
eyeL = filterLeftEye(face)
eyeR = filterRightEye(face)

cv2.rectangle(face.getImage(),(face.getFace()[0],face.getFace()[1]),(face.getFace()[0]+face.getFace()[2],face.getFace()[1]+face.getFace()[3]),(0,255,0),2)
cv2.rectangle(get_roi_color(face), (mouth[0],mouth[1]), (mouth[0]+mouth[2], mouth[1]+mouth[3]), (255, 0 ,0), 2)
cv2.rectangle(get_roi_color(face), (eyeL[0],eyeL[1]), (eyeL[0]+eyeL[2], eyeL[1]+eyeL[3]), (0,0,255), 2)
cv2.rectangle(get_roi_color(face), (eyeR[0],eyeR[1]), (eyeR[0]+eyeR[2], eyeR[1]+eyeR[3]), (0,0,255), 2)

cv2.imshow('img', face.getImage())
cv2.waitKey(0)
