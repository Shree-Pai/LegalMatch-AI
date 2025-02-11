import requests
import json

# Test the recommend_lawyers endpoint
def test_recommend_lawyers():
    url = 'http://localhost:5000/recommend_lawyers'
    data = {
        'case_type': 'Tax Law',
        'description': 'Need defense attorney for assault charges'
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test the predict_success endpoint
def test_predict_success():
    url = 'http://localhost:5000/predict_success'
    data = {
    "lawyer_id": 1,
    "case_type": "Civil",
    "complexity_score": 4.0
}

    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test invalid input (missing case_type)
def test_invalid_input_missing_case_type():
    url = 'http://localhost:5000/recommend_lawyers'
    data = {
        'description': 'Need defense attorney for assault charges'
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test invalid input (missing description)
def test_invalid_input_missing_description():
    url = 'http://localhost:5000/recommend_lawyers'
    data = {
        'case_type': 'Criminal Law'
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test the case where no lawyers are found
def test_no_lawyers_found():
    url = 'http://localhost:5000/recommend_lawyers'
    data = {
        'case_type': 'Unknown Case Type',
        'description': 'Some description for an unknown case type.'
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test the case where invalid lawyer_id is provided
def test_invalid_lawyer_id():
    url = 'http://localhost:5000/predict_success'
    data = {
        'lawyer_id': 9999,  # Assuming this ID does not exist
        'case_type': 'Criminal',
        'complexity_score': 5.0
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("Testing recommend_lawyers endpoint:")
    test_recommend_lawyers()
    print("\nTesting predict_success endpoint:")
    test_predict_success()
    print("\nTesting invalid input (missing case_type):")
    test_invalid_input_missing_case_type()
    print("\nTesting invalid input (missing description):")
    test_invalid_input_missing_description()
    print("\nTesting no lawyers found:")
    test_no_lawyers_found()
    print("\nTesting invalid lawyer_id:")
    test_invalid_lawyer_id()
