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
    url = '/predictor'
 
    response = client.get(url)
    sample_data = [[school], [traveltime], [studytime], [failures],
                   [schoolsup], [famsup], [paid], [activities], [higher], 
                   [internet], [freetime], [dalc], [walc], [absences]]
    student1 = [['GP'], [1], [2], [1], ['no'], ['yes'], ['yes'], ['yes'], 
                ['yes'], ['no'], ['yes'], [3], [1], [1], [6]]
    student2 = [['MS'], [2], [3], [2], ['no'], ['yes'], ['no'], ['yes'],
                ['yes'], ['no'], ['no'], [2], [1], [1], [4]]
    student3 = [['GP'], [2], [4], [4], ['yes'], ['yes'], ['yes'], ['yes'], 
                ['yes'], ['yes'], ['no'], [4], [1], [1], [10]]
    student4 = [['MS'], [4], [1], [4], ['no'], ['yes'], ['no'], ['yes'], 
                ['yes'], ['yes'], ['no'], [4], [1], [1], [10]]
    # invalid student 1: missing fields
    invalid_stu1 = [['GP'], [1], [2], [2], ['yes'], ['yes'], 
                    ['yes'], ['no'], ['yes'], [3], [2], [2], [18]]
    # invalid student 2: 'higher' field contain value other than 'yes' or 'no'
    invalid_stu2 = [['GP'], [1], [4], [1], ['yes'], ['yes'], ['yes'], ['yes'], 
                    ['na'], ['no'], ['yes'], [2], [1], [1], [5]]
    # invalid student 3: 'traveltime' field not in range 1 ~ 4 (inclusive) 
    invalid_stu3 = [['GP'], [5], [2], [1], ['no'], ['yes'], ['yes'], ['yes'], 
                    ['yes'], ['no'], ['yes'], [3], [1], [1], [6]]
    # invalid student 4: 'absences' field > 93
    invalid_stu4 = [['MS'], [2], [1], [3], ['no'], ['no'], ['no'], ['yes'], 
                    ['no'], ['no'], ['yes'], [4], [4], [4], [100]]
    # invalid student 5: 'dalc' and 'walc' fields wrong type
    invalid_stu5 = [['MS'], [1], [1], [2], ['no'], ['no'], ['no'], ['yes'], 
                    ['yes'], ['yes'], ['yes'], [4], ['yes'], ['yes'], [10]]
    assert response.status_code == 200
    assert response.get_data(sample_data) in {student1, student2, student3, student4}
    assert response.get_data(sample_data) not in {invalid_stu1, invalid_stu2, invalid_stu3, invalid_stu4, invalid_stu5}
    assert len(response.get_data(sample_data)) == 15
    # check each field in range / of allowed value
    assert response.get_data(sample_data)[0][0] in {'MS', 'GP'}
    assert response.get_data(sample_data)[1][0] in {1, 2, 3, 4}
    assert response.get_data(sample_data)[2][0] in {1, 2, 3, 4}
    assert response.get_data(sample_data)[3][0] in {1, 2, 3, 4}
    assert response.get_data(sample_data)[5][0] in {'yes', 'no'}
    assert response.get_data(sample_data)[6][0] in {'yes', 'no'}
    assert response.get_data(sample_data)[7][0] in {'yes', 'no'}
    assert response.get_data(sample_data)[8][0] in {'yes', 'no'}
    assert response.get_data(sample_data)[9][0] in {'yes', 'no'}
    assert response.get_data(sample_data)[10][0] in {'yes', 'no'}
    assert response.get_data(sample_data)[11][0] in {1, 2, 3, 4, 5}
    assert response.get_data(sample_data)[12][0] in {1, 2, 3, 4, 5}
    assert response.get_data(sample_data)[13][0] in {1, 2, 3, 4, 5}
    assert (0 <= response.get_data(sample_data)[14][0] <= 93)

    
    