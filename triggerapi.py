import threading, base64, json
from flask import Flask, jsonify, request
import requests
from main import wholetrigger,new
app = Flask(__name__)
from api import post_data
import base64

def base64url_decode(input_string):
    # Convert from Base64 URL-safe format to standard Base64 format
    input_string = input_string.replace('-', '+').replace('_', '/')

    # Padding the input string with '=' characters if necessary
    # Base64 URL-safe format does not include padding, so we calculate the padding needed
    padding_needed = 4 - (len(input_string) % 4)
    input_string += '=' * padding_needed

    # Decode the Base64 string
    decoded_bytes = base64.b64decode(input_string)

    # Convert bytes to a string
    decoded_string = decoded_bytes.decode('utf-8')  # Adjust encoding as necessary

    return decoded_string


# Route to trigger the function
@app.route('/wholetrigger', methods=['GET'])
def whole_trigger():
    response = jsonify({"message": "wholetrigger function executed successfully."})
    # Create and start a new thread to run the wholetrigger function
    trigger_thread = threading.Thread(target=wholetrigger)
    trigger_thread.start()
    return response

def process_response(api_url, headers, data):
    try:
        response = requests.get(api_url, headers=headers, json=data)   

        if response.status_code == 200:

            try:
                response_data =json.loads(base64url_decode(response.text))
                # print("Data:", response_data)
                # Process the response_data as needed
                one_user_unique_data=new(response_data) #data comes in list format which postable
                print('one user unique data',one_user_unique_data, len(one_user_unique_data))
                #to post the one user with one event unique data
                post_data(one_user_unique_data)
            except ValueError as e:
                print("Error: Response is not in JSON format")
                # print(f"Response content: {response.text}")
        else:
            print(f"Error: GET request failed with status code {response.status_code}")
            print("Response content:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

@app.route('/singleuserimage/<EventId>/<UserId>', methods=['POST'])
def receive_data(EventId, UserId):
    data = request.get_json() if request.is_json else {}
    data['EventId'] = EventId
    data['UserId'] = UserId
    
    api_url = f"http://192.168.1.29:8083/api/facedetection/getAllEventFolderAndOneUseImage/{UserId}"
    headers = {
        "Content-Type": "application/json",
    }
    data = {"eventId": EventId}
    
    # Start a new thread to process the response
    threading.Thread(target=process_response, args=(api_url, headers, data)).start()
    # Return success immediately
    return 'success single user checking with event data has started'

if __name__ == '__main__':
    app.run(host='192.168.1.29', port=5000, debug=True)