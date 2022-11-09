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

def test_predict_route_valid1():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    # Summary of query string: Valid - expected 0 as return value
    # absences: 10, school: GP, studytime: 2, traveltime: 2, schoolsup: yes, 
    # famsup: yes, paid: yes, higher: yes, internet: yes, freetime: 2, Dalc: 1, 
    # Walc: 1
    query = '?absences=10&school=GP&studytime=2&traveltime=2&schoolsup=yes&famsup=yes&paid=yes&activities=no&higher=yes&internet=yes&freetime=2&Dalc=1&Walc=1'
    response = client.get(url+query)

    assert response.status_code == 200
    assert response.get_data() == b'0\n'

    
def test_predict_route_valid2():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    # Summary of query string: Valid - expected 0 as return value
    # absences: 6, school: MS, studytime: 2, traveltime: 1, schoolsup: yes, 
    # famsup: yes, paid: yes, higher: yes, internet: yes, freetime: 2, Dalc: 1, 
    # Walc: 2
    query = '?absences=6&school=MS&studytime=2&traveltime=1&schoolsup=yes&famsup=yes&paid=yes&activities=yes&higher=yes&internet=yes&freetime=2&Dalc=1&Walc=2'
    response = client.get(url+query)
    assert response.status_code == 200
    assert response.get_data() == b'0\n'

def test_predict_route_missing_school():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    # Summary of query string: Error - missing school parameter - expected warning string
    # absences: 6, studytime: 2, traveltime: 2, schoolsup: yes, famsup: no
    # paid: yes, higher: yes, internet: yes, freetime: 2, Dalc: 1, Walc: 1
    query = '?absences=15&studytime=2&traveltime=2&schoolsup=yes&famsup=no&paid=yes&activities=yes&higher=yes&internet=yes&freetime=2&Dalc=1&Walc=1'
    response = client.get(url+query)
    assert response.status_code == 200
    assert response.get_data() == b'Invalid school: expected MS or GP'

def test_predict_route_famsup_nonbinary():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    # Summary of query string: Error - answer of family support other than yes or no - expected warning string
    # absences: 8, school: MS, studytime: 3, traveltime: 1, schoolsup: yes, 
    # famsup: na, paid: yes, higher: yes, internet: yes, freetime: 3, Dalc: 1, 
    # Walc: 1
    query = '?absences=8&school=MS&studytime=3&traveltime=1&schoolsup=yes&famsup=na&paid=yes&activities=yes&higher=yes&internet=yes&freetime=3&Dalc=1&Walc=1'
    response = client.get(url+query)
    assert response.status_code == 200
    assert response.get_data() == b'Invalid family support status: expected yes or no'

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
