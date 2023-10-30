from flask import Flask, request, app,render_template
from flask_cors import CORS,cross_origin
from flask import Response
import pickle
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

application = Flask(__name__)
app=application
CORS(app)

scaler=joblib.load("standardScalar.pkl")
model = joblib.load("modelForPrediction.pkl")

## Route for homepage

@app.route('/', methods = ['GET'])
@cross_origin()
def index():
    return render_template('home.html')
    
## Route for Single data point prediction
@app.route('/predictdata',methods=['GET','POST'])
@cross_origin()
def predict_datapoint():
    result=""

    if request.method=='POST':

        Pregnancies=int(request.form.get("Pregnancies"))
        Glucose = float(request.form.get('Glucose'))
        BloodPressure = float(request.form.get('BloodPressure'))
        SkinThickness = float(request.form.get('SkinThickness'))
        Insulin = float(request.form.get('Insulin'))
        BMI = float(request.form.get('BMI'))
        DiabetesPedigreeFunction = float(request.form.get('DiabetesPedigreeFunction'))
        Age = float(request.form.get('Age'))

        new_data=scaler.transform([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]])
        predict=model.predict(new_data)
       
        if predict[0] ==1 :
            result = 'Diabetic'
        else:
            result ='Non-Diabetic'
            
        return render_template('single_prediction.html',result=result)

    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)