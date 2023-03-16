import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,render_template,request

import cv2
from flask import Flask, render_template

app=Flask(__name__)

model=load_model("predicter.h5")
  
@app.route('/')
def index():
    return render_template("index.html")
text=''
@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['image']
        img=image.load_img(f,target_size=(,))
        x=image.img_to_array(img)
        x = np.expand_dims(x,axis=0)
        pred = model.predict(x)
        y = int(pred[0][0])
        if(pred==1):
            text='OK'
        else:
            text='NO FIRE'
    return text

if __name__=='__main__':
    app.run(debug=False)
