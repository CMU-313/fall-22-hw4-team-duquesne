import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"


    @app.route('/predictor')
    def predict():
        #use entries from the query string here but could also use json
        #useful data: school, traveltime, studytime, schoolsup, famsup, paid, 
        #             activities, higher, internet, freetime, Dalc, Walc,
        #             absences
        # age = request.args.get('age')
        # health = request.args.get('health')
        school = request.args.get('school')
        traveltime = request.args.get('travaltime')
        studytime = request.args.get('studytime')
        schoolsup = request.args.get('schoolsup')
        famsup = request.args.get('famsup')
        paid = request.args.get('paid')
        activities = request.args.get('activities')
        higher = request.args.get('higher')
        internet = request.args.get('internet')
        freetime = request.args.get('freetime')
        dalc = request.args.get('Dalc')
        walc = request.args.get('Walc')
        absences = request.args.get('absences')
        data = [[school], [traveltime], [studytime], [schoolsup], [famsup], 
                [paid], [activities], [higher], [internet], [freetime],
                [dalc], [walc], [absences]]
        query_df = pd.DataFrame({
            'school': pd.Series(school),
            'traveltime': pd.Series(traveltime),
            'studytime': pd.Series(studytime),
            'schoolsup': pd.Series(famsup),
            'paid': pd.Series(paid),
            'activities': pd.Series(activities),
            'higher': pd.Series(higher),
            'internet': pd.Series(internet),
            'freetime': pd.Series(freetime),
            'dalc': pd.Series(dalc),
            'walc': pd.Series(walc),
            'absences': pd.Series(absences)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))