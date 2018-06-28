import cv2
import PIL.Image
import PIL.ImageTk
import tkinter as tk
import wb_ui_support
import os
scaleX = 0.6
scaleY = 0.75

CurrentFilePath = os.getcwd()
cascadePath = CurrentFilePath+"/WashingBot/haarcascade/haarcascade_frontalface_default.xml"
eyeCascadePath = CurrentFilePath+'/WashingBot/haarcascade/haarcascade_eye.xml'
eye_cascade = cv2.CascadeClassifier(eyeCascadePath)
faceCascade = cv2.CascadeClassifier(cascadePath);
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read(CurrentFilePath+'/WashingBot/recognizer/trainingData.yml')


#for inputText
h_offset  = 150
font      = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (0, 255, 0)
thickness = 2


def update_image(image_label, cv_capture):
    cv_image = cv_capture.read()[1]
    cv_image = cv2.flip(cv_image, 1)


    gray=cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(cv_image,(x,y),(x+w,y+h),(225,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = cv_image[y:y+h, x:x+w]
        id,conf = rec.predict(gray[y:y+h,x:x+w])
        # cv_image = cv2.resize(cv_image,None,fx=scaleX,fy=scaleY,interpolation=cv2.INTER_LINEAR)

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        name = 'Unknow'
        nameID = 'Unknow'
        gender = 'Unknow'
        live = 'Unknow'

        if (id==1):
            name = 'Thar Htet San'
            nameID = '4esy-2'
            gender = 'Male'
            live = 'UCSM'
        elif(id == 10):
            name = 'Myat Thiha Naing'
            nameID = 'Unknow'
            gender = 'Unknow'
            live = 'Unknow'
        v_offset= y+h
        h_offset = x
        cv2.putText(cv_image,str(name),(h_offset,v_offset),font,fontScale,fontColor,thickness)
        v_offset += 20
        cv2.putText(cv_image,str(nameID),(h_offset,v_offset),font,fontScale,fontColor,thickness)
        v_offset += 20
        cv2.putText(cv_image,str(gender),(h_offset,v_offset),font,fontScale,fontColor,thickness)
        v_offset += 20
        cv2.putText(cv_image,str(live),(h_offset,v_offset),font,fontScale,fontColor,thickness)



    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    pil_image = PIL.Image.fromarray(cv_image)
    tk_image = PIL.ImageTk.PhotoImage(image=pil_image)
    image_label.configure(image=tk_image)
    image_label._image_cache = tk_image  # avoid garbage collection
    wb_ui_support.root.update()


def update_all(root, image_label, cv_capture):
    if wb_ui_support.root.quit_flag:
        wb_ui_support.root.destroy()  # this avoids the update event being in limbo
    else:
        update_image(image_label, cv_capture)
        wb_ui_support.root.after(10, func=lambda: update_all(root, image_label, cv_capture))
