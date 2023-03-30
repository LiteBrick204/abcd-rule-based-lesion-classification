import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from ABCD_rule import getABCDValue
import cv2
from flask import Flask, render_template, request, Response

app=Flask(__name__)

model=load_model("predictor_2.h5")

@app.route('/')
def index():
    return render_template("index.html")
text=''
@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['image'] 
        filepath=os.path.join('images/',f.filename)
        print(filepath)
        f.save(filepath)
        img=image.load_img(filepath,target_size=(64,64)) 
        x=image.img_to_array(img)
        result_a,result_b,result_c,result_d=getABCDValue(filepath)
        x = np.expand_dims(x,axis=0)
        pred = model.predict(x)
        y = np.argmax(pred)
        choices = ['lentigo NOS', 'lichenoid keratosis', 'melanoma', 'nevus', 'seborrheic keratosis', 'solar lentigo']
        TDS = (float(result_a)*1.3) + (float(result_b)*0.1) + (float(result_c)*0.5) + (float(result_d)*0.5) 
        TDS = "{:.2f}".format(TDS) 
        if float(TDS)<=4.5:
            Type="Benign"
        else:
            Type="Malignant"
        resp = Response(f"{choices[y]}\n\n\n\n Asymmetry:{result_a}\n\n\n\n\n Border:{result_b}\n\n\n\n\nColor:{result_c}\n\n\n\n\n\nDiameter:{result_d}\n\n\n\n\n\n TDSValue:{TDS}\n\n\n\n\n\n Benign/Malignant: {Type}")
        resp.headers['Content-Type'] = 'text/html'
    return resp

if __name__=='__main__':
    app.run(debug=False)
