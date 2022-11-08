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


    @app.route('/predict', methods = ['POST', 'GET'])
    def predict():
        #use entries from the query string here but could also use json
        #useful data: school, traveltime, studytime, schoolsup, famsup, paid, 
        #             activities, higher, internet, freetime, Dalc, Walc,
        #             absences
        # numerical values
        absences = request.args.get('absences')
        traveltime = request.args.get('travaltime')
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
        
        schoolsup_no, schoolsup_yes, schoolsup_nan = 0,0
        if schoolsup == 'yes':
            schoolsup_yes = 1
        elif schoolsup == 'no':
            schoolsup_no = 1
        else:
            schoolsup_nan = 1
        
        activities_no, activities_yes, actitvities_nan = 0,0,0

        if activities == 'yes':
            activities_yes = 1
        elif activities == 'no':
            activities_no = 1
        else:
            activities_nan = 1

        famsup_no, famsup_yes, famsup_nan = 0,0,0
        if famsup == 'yes':
            famsup_yes = 1
        elif famsup == 'no':
            famsup_no = 1
        else:
            famsup_nan = 1
        

        higher_no, higher_yes, famsup_nan = 0,0,0
        if higher == 'yes':
            higher_yes = 1
        elif higher == 'no':
            higher_no = 1
        else:
            higher_nan = 1

        internet_no, internet_yes, internet_nan = 0,0,0
        if internet == 'yes':
            internet_yes = 1
        elif internet == 'no':
            internet_no = 1
        else:
            internet_nan = 1
        
        paid_no, paid_yes, paid_nan = 0,0,0
        if paid == 'yes':
            paid_yes = 1
        elif paid == 'no':
            paid_no = 1
        else:
            paid_nan = 1
        
        school_GP, school_MS, school_nan = 0,0,0
        if school == 'GP':
            school_GP = 1
        elif school == 'MS':
            school_MS = 1
        else:
            school_nan = 1
        print(absences)
        data = [[traveltime], [studytime],[freetime],[dalc],[walc], [absences]]
        query_df = pd.DataFrame(data = {
            'traveltime': pd.Series(traveltime),
            'studytime': pd.Series(studytime),
            'freetime': pd.Series(freetime),
            'Dalc': pd.Series(dalc),
            'Walc': pd.Series(walc),
            'absences': pd.Series(absences)
            },
            index = ['traveltime', 'studytime', 'freetime', 'Dalc', 'Walc', 'absences'])
        query = pd.get_dummies(query_df)
        print(query_df)
        print(query)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))
        # school = request.args.get('school')
        # traveltime = request.args.get('travaltime')
        # studytime = request.args.get('studytime')
        # schoolsup = request.args.get('schoolsup')
        # famsup = request.args.get('famsup')
        # paid = request.args.get('paid')
        # activities = request.args.get('activities')
        # higher = request.args.get('higher')
        # internet = request.args.get('internet')
        # freetime = request.args.get('freetime')
        # dalc = request.args.get('Dalc')
        # walc = request.args.get('Walc')
        
        # schoolsup_no, schoolsup_yes, schoolsup_nan = 0,0
        # if schoolsup == 'yes':
        #     schoolsup_yes = 1
        # elif schoolsup == 'no':
        #     schoolsup_no = 1
        # else:
        #     schoolsup_nan = 1
        
        # activities_no, activities_yes, actitvities_nan = 0,0,0

        # if activities == 'yes':
        #     activities_yes = 1
        # elif activities == 'no':
        #     activities_no = 1
        # else:
        #     activities_nan = 1

        # famsup_no, famsup_yes, famsup_nan = 0,0,0
        # if famsup == 'yes':
        #     famsup_yes = 1
        # elif famsup == 'no':
        #     famsup_no = 1
        # else:
        #     famsup_nan = 1
        

        # higher_no, higher_yes, famsup_nan = 0,0,0
        # if higher == 'yes':
        #     higher_yes = 1
        # elif higher == 'no':
        #     higher_no = 1
        # else:
        #     higher_nan = 1

        # internet_no, internet_yes, internet_nan = 0,0,0
        # if internet == 'yes':
        #     internet_yes = 1
        # elif internet == 'no':
        #     internet_no = 1
        # else:
        #     internet_nan = 1
        
        # paid_no, paid_yes, paid_nan = 0,0,0
        # if paid == 'yes':
        #     paid_yes = 1
        # elif paid == 'no':
        #     paid_no = 1
        # else:
        #     paid_nan = 1
        
        # school_GP, school_MS, school_nan = 0,0,0
        # if school == 'GP':
        #     school_GP = 1
        # elif school == 'MS':
        #     school_MS = 1
        # else:
        #     school_nan = 1

        # data = [[dalc], [walc], [absences], [freetime], [studytime], 
        #         [traveltime], [activities_no], [activities_yes], 
        #         [famsup_no], [famsup_yes], [higher_no], [higher_yes],
        #         [internet_no], [internet_yes], [paid_no], [paid_yes],
        #         [school_GP], [school_MS], [schoolsup_no], [schoolsup_yes]]
        # query_df = pd.DataFrame({'Dalc': pd.Series(dalc), 'Walc': pd.Series(walc), 'absences': pd.Series(absences), 'freetime': pd.Series(freetime),
        #                   'studytime': pd.Series(studytime), 'traveltime': pd.Series(traveltime),
        #                   'activities_no': pd.Series(activities_no), 'activities_yes': pd.Series(activities_yes),
        #                   'famsup_no': pd.Series(famsup_no), 'famsup_yes': pd.Series(famsup_yes), 
        #                   'higher_no': pd.Series(higher_no), 'higher_yes': pd.Series(higher_yes),
        #                   'internet_no': pd.Series(internet_no), 'internet_yes': pd.Series(internet_yes),
        #                   'paid_no': pd.Series(paid_no), 'paid_yes': pd.Series(paid_yes),
        #                   'school_GP' : pd.Series(school_GP), 'school_MS': pd.Series(school_MS),
        #                   'schoolsup_no': pd.Series(schoolsup_no), 'schoolsup_yes': pd.Series(schoolsup_yes)} )
        # # query_df = pd.DataFrame({
        # #     'school': pd.Series(school),
        # #     'traveltime': pd.Series(traveltime),
        # #     'studytime': pd.Series(studytime),
        # #     'schoolsup': pd.Series(famsup),
        # #     'paid': pd.Series(paid),
        # #     'activities': pd.Series(activities),
        # #     'higher': pd.Series(higher),
        # #     'internet': pd.Series(internet),
        # #     'freetime': pd.Series(freetime),
        # #     'Dalc': pd.Series(dalc),
        # #     'Walc': pd.Series(walc),
        # #     'absences': pd.Series(absences)
        # # })
        # query = pd.get_dummies(query_df)
        # print(query)
        # prediction = clf.predict(query)
        # return jsonify(np.asscalar(prediction))
        