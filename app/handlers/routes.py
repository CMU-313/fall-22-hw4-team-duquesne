import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os
import string

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"


    @app.route('/predict', methods = ['POST', 'GET'])
    def predict():
        #useful data: school, traveltime, studytime, schoolsup, famsup, paid, 
        #             activities, higher, internet, freetime, Dalc, Walc,
        #             absences
        # numerical values
        absences = request.args.get('absences')
        traveltime = request.args.get('traveltime')
        studytime = request.args.get('studytime')
        dalc = request.args.get('Dalc')
        walc = request.args.get('Walc')
        freetime = request.args.get('freetime')
        # non-numerical values - categorical
        school = request.args.get('school')
        schoolsup = request.args.get('schoolsup')
        famsup = request.args.get('famsup')
        paid = request.args.get('paid')
        activities = request.args.get('activities')
        higher = request.args.get('higher')
        internet = request.args.get('internet')

        # Handle out-of-range numerical input when necessary
        if (not absences.isnumeric()) or int(absences) < 0 or int(absences) > 93:
            return 'Invalid days of absences: expected integer between 0 - 93'
        
        if (not traveltime.isnumeric()) or int(traveltime) < 0 or int(traveltime) >= 5:
            return 'Invalid travel time: expected integer between 1 - 4'

        if (not studytime.isnumeric()) or int(studytime) < 0 or int(studytime) >= 5:
            return 'Invalid study time: expected integer between 1 - 4'
        
        if (not freetime.isnumeric()) or int(freetime) < 0 or int(freetime) >= 5:
            return 'Invalid free time: expected integer between 1 - 4'
        
        if (not dalc.isnumeric()) or int(dalc) < 0 or int(dalc) >= 5:
            return 'Invalid daily alcohol consumption: expected integer between 1 - 4'
        
        if (not walc.isnumeric()) or int(walc) < 0 or int(walc) >= 5:
            return 'Invalid weekly alcohol consumption: expected integer between 1 - 4'
        
        # convert binary categorical data into binary number
        # handle invalid input when necessary
        schoolsup_no, schoolsup_yes, schoolsup_nan = 0,0,0
        if schoolsup == 'yes':
            schoolsup_yes = 1
        elif schoolsup == 'no':
            schoolsup_no = 1
        else:
            return 'Invalid school support status: expected yes or no'
       
        activities_no, activities_yes, actitvities_nan = 0,0,0

        if activities == 'yes':
            activities_yes = 1
        elif activities == 'no':
            activities_no = 1
        else:
            return 'Invalid activities status: expected yes or no'

        famsup_no, famsup_yes, famsup_nan = 0,0,0
        if famsup == 'yes':
            famsup_yes = 1
        elif famsup == 'no':
            famsup_no = 1
        else:
            return 'Invalid family support status: expected yes or no'
        
        higher_no, higher_yes, famsup_nan = 0,0,0
        if higher == 'yes':
            higher_yes = 1
        elif higher == 'no':
            higher_no = 1
        else:
            return 'Invalid higher education status: expected yes or no'

        internet_no, internet_yes, internet_nan = 0,0,0
        if internet == 'yes':
            internet_yes = 1
        elif internet == 'no':
            internet_no = 1
        else:
            return 'Invalid internet status: expected yes or no'
        
        paid_no, paid_yes, paid_nan = 0,0,0
        if paid == 'yes':
            paid_yes = 1
        elif paid == 'no':
            paid_no = 1
        else:
            return 'Invalid paid status: expected yes or no'
        
        school_GP, school_MS, school_nan = 0,0,0
        if school == 'GP':
            school_GP = 1
        elif school == 'MS':
            school_MS = 1
        else:
            return 'Invalid school: expected MS or GP'

        data = [[dalc], [walc], [absences],
                [freetime], [studytime], [traveltime], 
                [activities_no], [activities_yes], 
                [famsup_no], [famsup_yes], 
                [higher_no], [higher_yes], 
                [internet_no], [internet_yes], 
                [paid_no], [paid_yes], 
                [school_GP], [school_MS], 
                [schoolsup_no], [schoolsup_yes]]

        query_df = pd.DataFrame(data = {
            'Dalc': pd.Series(dalc),
            'Walc': pd.Series(walc),
            'absences': pd.Series(absences),
            'freetime': pd.Series(freetime),
            'studytime': pd.Series(studytime),
            'traveltime': pd.Series(traveltime),
            'activities_no': pd.Series(activities_no),
            'activities_yes': pd.Series(activities_yes),
            'famsup_no': pd.Series(famsup_no),
            'famsup_yes': pd.Series(famsup_yes),
            'higher_no': pd.Series(higher_no),
            'higher_yes': pd.Series(higher_yes),
            'internet_no': pd.Series(internet_no),
            'internet_yes': pd.Series(internet_yes),
            'paid_no': pd.Series(paid_no),
            'paid_yes': pd.Series(paid_yes),
            'school_GP': pd.Series(school_GP),
            'school_MS': pd.Series(school_MS),
            'schoolsup_no': pd.Series(schoolsup_no),
            'schoolsup_yes': pd.Series(schoolsup_yes)
            },
            index = [0])
        # query = pd.get_dummies(query_df)
        # print(query)
        prediction = clf.predict(query_df)
        return jsonify(np.ndarray.item(prediction))

        