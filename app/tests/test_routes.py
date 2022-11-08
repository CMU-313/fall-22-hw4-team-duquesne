from flask import Flask

from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    
    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
 
    response = client.get(url)
    correctJson = [{"traveltime": 2, "studytime": 2, "freetime": 3, 
                    "Dalc": 1, "Walc": 1, "absences": 6}, # line 1, G3 = 6
                   {"traveltime": 1, "studytime": 3, "freetime": 2, 
                    "Dalc": 1, "Walc": 1, "absences": 5}, # line 5, G3 = 15
                   {"traveltime": 1, "studytime": 2, "freetime": 3, 
                    "Dalc": 1, "Walc": 2, "absences": 0}, # line 12, G3 = 9
                  ]

    assert response.status_code == 200
    assert response.post(url, data=correctJson) == {"prediction": [{6}, {15}, {9}]}

    # correctJson = [
    # {"school": "GP", "traveltime": 1, "studytime": 2, "schoolsup": "no", "famsup": "no", "paid": "yes", 
    # "activities": "yes", "higher": "yes", "internet": "yes", "freetime": 3, "dalc": 3, "walc": 4, "absences": 12},
    # {"school": "MS", "traveltime": 3, "studytime": 1, "schoolsup": "yes", "famsup": "yes", "paid": "yes", 
    # "activities": "yes", "higher": "yes", "internet": "yes", "freetime": 3, "dalc": 3, "walc": 5, "absences": 93},
    # {"school": "MS", "traveltime": 3, "studytime": 4, "schoolsup": "no", "famsup": "no", "paid": "yes", 
    # "activities": "no", "higher": "no", "internet": "no", "freetime": 3, "dalc": 3, "walc": 4, "absences": 0},
    # {"school": "MS", "traveltime": 3, "studytime": 0, "schoolsup": "yes", "famsup": "no", "paid": "yes", 
    # "activities": "no", "higher": "no", "internet": "no", "freetime": 3, "dalc": 3, "walc": 4, "absences": 0}, 
    # {"school": "GP", "traveltime": 1, "studytime": 0, "schoolsup": "no", "famsup": "no", "paid": "yes", 
    # "activities": "no", "higher": "no", "internet": "no", "freetime": 3, "dalc": 3, "walc": 4, "absences": 0}, 
    # {"school": "GP", "traveltime": 2, "studytime": 4, "schoolsup": "yes", "famsup": "no", "paid": "yes", 
    # "activities": "no", "higher": "no", "internet": "no", "freetime": 3, "dalc": 3, "walc": 4, "absences": 0}, 
    # {"school": "GP", "traveltime": 1, "studytime": 4, "schoolsup": "yes", "famsup": "no", "paid": "yes", 
    # "activities": "no", "higher": "no", "internet": "no", "freetime": 3, "dalc": 3, "walc": 4, "absences": 0}, 
    # {"school": "MS", "traveltime": 3, "studytime": 4, "schoolsup": "yes", "famsup": "no", "paid": "yes", 
    # "activities": "no", "higher": "no", "internet": "no", "freetime": 3, "dalc": 3, "walc": 4, "absences": 0}
    # ]

    # # invalid studytime 
    # badStudy = [{"school": "MS", "traveltime": 3, "studytime": -8, "schoolsup": "yes", "famsup": "yes", "paid": "yes", 
    # "activities": "yes", "higher": "yes", "internet": "yes", "freetime": 3, "dalc": 3, "walc": 5, "absences": 93}]
    # #invalid internet 
    # badInternet = [{"school": "MS", "traveltime": 3, "studytime": 8, "schoolsup": "yes", "famsup": "yes", "paid": "yes", 
    # "activities": "yes", "higher": "yes", "internet": "YES", "freetime": 3, "dalc": 3, "walc": 5, "absences": 93}]
    # #invalid schoolsup
    # badSchoolsUp = [{"school": "MS", "traveltime": 3, "studytime": 8, "schoolsup": "pl", "famsup": "yes", "paid": "yes", 
    # "activities": "yes", "higher": "yes", "internet": "yes", "freetime": 3, "dalc": 3, "walc": 5, "absences": 93}]
    # #invalid walc
    # badWalc = [{"school": 12, "traveltime": 0, "studytime": 4, "schoolsup": "yes", "famsup": "no", "paid": "yes", 
    # "activities": "no", "higher": "no", "internet": "no", "freetime": 3, "dalc": 3, "walc": "yo", "absences": 0}]
   
    # assert response.status_code == 200
    
    # assert response.post(url, data=correctJson) == {"prediction": [12, 9, 5, 18, 19, 3, 5, 7]}
    # assert response.post(url, data=badStudy) == {"prediction": [0]}
    # assert response.post(url, data=badInternet) == {"prediction": [0]}
    # assert response.post(url, data=badSchoolsUp) == {"prediction": [0]}
    # assert response.post(url, data=badWalc) == {"prediction": [0]}
