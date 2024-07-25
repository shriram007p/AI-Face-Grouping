import requests
import json


def get_admin_ids():
    # Replace with the actual API URL you want to access
    api_url = "http://192.168.1.29:8083/api/facedetection/getAllAdminId"

    # Set headers dictionary (replace with any required headers)
    headers = {
        "Content-Type": "application/json",
    }

    # Make a GET request to the API endpoint with headers
    response = requests.get(api_url, headers=headers)

    # Check for successful response status code
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()  # Use .json() to directly parse JSON response
    else:
        data = None
    return data


def get_event_ids(admin_id):
    # Replace with the actual API URL you want to access
    api_url = "http://192.168.1.29:8083/api/facedetection/getEventId"

    # Set headers dictionary (replace with any required headers)
    headers = {
        "Content-Type": "application/json",
        "Create-by-id": str(admin_id)  # Replace with admin ID
    }

    # Make a GET request to the API endpoint with headers
    response = requests.get(api_url, headers=headers)

    # Check for successful response status code
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()  # Use .json() to directly parse JSON response
    else:
        data = None

    return data


def get_event_and_user_image(admin_id, event_id):
    # Replace with the actual API URL you want to access
    api_url = "http://192.168.1.29:8083/api/facedetection/getEventFolderImage"

    # Set headers dictionary (replace with any required headers)
    headers = {
        "Content-Type": "application/json",
        "Create-by-id": str(admin_id)
    }
    # Create request body dictionary (replace with your data)
    data = {
        "eventId": event_id }

    # Make a POST request to the API endpoint with headers and body
    response = requests.get(api_url, headers=headers, json=data)

    # Check for successful response status code
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

    else:
        data = None

    return data


def post_data(data_list):
    print("post data to db",data_list)
   
    api_url = "http://192.168.1.29:8083/api/facedetection/setuserEventImage"

    # Set headers dictionary (replace with any required headers)
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request with data and headers
    response = requests.post(api_url, headers=headers, json=data_list)
    # Check the response status
    if response.status_code == 200: 
        print(response.status_code)
        print("Data posted successfully")

    else:
        print("Failed to post data")
