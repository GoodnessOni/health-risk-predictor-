from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load models
heart_model = joblib.load('heart_risk_model.pkl')
muscle_model = joblib.load('muscle_weakness_rf_model.pkl')

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Heart Risk
@app.route('/heart-risk', methods=['GET', 'POST'])
def heart_risk():
    result = None
    if request.method == 'POST':
        try:
            # Get form data
            HighBP = int(request.form['HighBP'])
            HighChol = int(request.form['HighChol'])
            Diabetes_012 = int(request.form['Diabetes_012'])
            BMI = float(request.form['BMI'])
            Smoker = int(request.form['Smoker'])
            GenHlth = int(request.form['GenHlth'])
            Age = int(request.form['Age'])
            DiffWalk = int(request.form['DiffWalk'])

            # Prepare input
            input_data = [[HighBP, HighChol, Diabetes_012, BMI, Smoker, GenHlth, Age, DiffWalk]]

            # Make prediction
            prediction_raw = heart_model.predict(input_data)[0]
            result = 'At Risk' if prediction_raw == 1 else 'Not at Risk'

            # Save to history
            record = input_data[0] + ['Heart Risk', result, datetime.now()]
            pd.DataFrame([record]).to_csv('history.csv', mode='a', header=False, index=False)

            # Redirect to result page
            return redirect(url_for('predict_heart_summary', prediction=result))

        except Exception as e:
            result = f"Error: {e}"

    # GET request — show the form
    return render_template('heart_risk.html', result=result)

""" @app.route('/predict-heart', methods=['GET'])
def predict_heart():
    # collect form data
    highbp = int(request.form.get('HighBP', 0))
    highchol = int(request.form.get('HighChol', 0))
    diabetes = int(request.form.get('Diabetes_012', 0))
    bmi = float(request.form.get('BMI', 0))
    smoker = int(request.form.get('Smoker', 0))
    genhlth = int(request.form.get('GenHlth', 0))
    age = int(request.form.get('Age', 0))
    diffwalk = int(request.form.get('DiffWalk', 0))
    result = 'High Risk'  # or 'Low Risk' 

    import csv
    with open('history.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            highbp, highchol, diabetes, bmi, smoker,
            genhlth, age, diffwalk,
            'Heart Risk', result,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ])

    return render_template('result.html', result=result) """

@app.route("/predict-heart-summary", methods=["GET"])
def predict_heart_summary():
    prediction = request.args.get("prediction", "")
    if prediction == "At Risk":
        message = "⚠️ You have a high probability of getting heart disease. Don't know what to do next? Visit our Health Tips page."
    else:
        message = "🎉 Congratulations! You have a very low probability of having heart disease. To keep up this great health, visit our Health Tips page for more tips."

    return render_template("result.html", prediction=prediction, message=message,  condition="Heart Disease")           

# Muscle Weakness
@app.route('/muscle-weakness', methods=['GET', 'POST'])
def muscle_weakness():
    result = None
    if request.method == 'POST':
        try:
            # Get form data
            PhysActivity = int(request.form['PhysActivity'])
            BMI = float(request.form['BMI'])
            PhysHlth = int(request.form['PhysHlth'])
            MentHlth = int(request.form['MentHlth'])
            Age = int(request.form['Age'])
            HighBP = int(request.form['HighBP'])
            GenHlth = int(request.form['GenHlth'])
            Diabetes_012 = int(request.form['Diabetes_012'])
            Smoker = int(request.form['Smoker'])
            Income = int(request.form['Income'])

            # Prepare input
            input_data = [[PhysActivity, BMI, PhysHlth, MentHlth, Age, HighBP, GenHlth, Diabetes_012, Smoker, Income]]

            # Make prediction
            prediction_raw = muscle_model.predict(input_data)[0]
            result = 'At Risk' if prediction_raw == 1 else 'Not at Risk'

            # Save to history
            record = input_data[0] + ['Muscle Weakness', result, datetime.now()]
            pd.DataFrame([record]).to_csv('history.csv', mode='a', header=False, index=False)

            # Redirect to result page
            return redirect(url_for('predict_muscle_summary', prediction=result))

        except Exception as e:
            result = f"Error: {e}"

    return render_template('muscle_weakness.html', result=result)

@app.route("/predict-muscle-summary", methods=["GET"])
def predict_muscle_summary():
    prediction = request.args.get("prediction", "")
    if prediction == "At Risk":
        message = "⚠️ You may be at risk of muscle weakness or mobility issues. Consider reviewing your physical activity and health habits."
    else:
        message = "🎉 Great news! You have a low risk of muscle weakness. Keep up the healthy lifestyle!"

    return render_template("result.html", prediction=prediction, message=message,  condition="Muscle Weakness")





# History
def decode_row(row):
    mappings = {
        '0': 'No',
        '1': 'Yes',
        '2': 'Often',
        '3': 'Rarely',
        '0.0': 'No',
        '1.0': 'Yes'
    }

    # Adjust these indices based on your CSV structure
    categorical_indices = [0, 5, 6, 7, 8, 9]  # Example: PhysActivity, HighBP, GenHlth, Diabetes, Smoker, Income

    decoded = []
    for i, val in enumerate(row):
        if i in categorical_indices:
            decoded.append(mappings.get(str(val).strip(), val))
        else:
            decoded.append(val)
    return decoded

from flask import render_template

@app.route('/history')
def show_history():
    try:
        with open('history.csv', 'r') as f:
            lines = [line.strip().split(',') for line in f.readlines()]
        
        # Decode categorical values
        decoded_records = [decode_row(row) for row in lines]

        # Separate by prediction type
        heart_history = [row for row in decoded_records if len(row) >= 11 and 'heart' in row[-3].lower()]
        muscle_history = [row for row in decoded_records if len(row) >= 13 and 'muscle' in row[-3].lower()]
    
    except FileNotFoundError:
        heart_history = []
        muscle_history = []

    return render_template('history.html', heart_history=heart_history, muscle_history=muscle_history)



@app.route('/clear-history', methods=['POST'])
def clear_history():
    try:
        with open('history.csv', 'w') as f:
            f.truncate()  # Clears the file
    except FileNotFoundError:
        pass
    return redirect(url_for('show_history'))



from flask import send_file

@app.route('/download-history')
def download_history():
    try:
        return send_file('history.csv', as_attachment=True)
    except FileNotFoundError:
        return "No history file found.", 404


# Tips
@app.route('/tips')
def tips():
    return render_template('health_tips.html')



@app.route("/health-tips")
def health_tips():
    return render_template("health_tips.html")





if __name__ == '__main__':
    app.run(debug=True)
# Ensure the app runs only if this file is executed directly


