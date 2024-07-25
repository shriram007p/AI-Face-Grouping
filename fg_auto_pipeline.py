from torch import cosine_similarity
from convert_Base64ToImage import convert_Base64ToImgae
import cv2
import numpy as np
import face_recognition

def face_encoding(image):
    # face encoding with face_recognition
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    encodings = face_recognition.face_encodings(rgb_image, face_locations)
    return encodings

def event_encode_faces_preprocess(encoded_string,single_image_data):
    oneimage = convert_Base64ToImgae(encoded_string)
    
    nescessary_data=[]
    if oneimage is not None:
        encodings = face_encoding(oneimage)
        # cv2.imshow('ft 
 
        if encodings:
            print('encodings lenght:',len(encodings))

            for encoding in encodings:
                encoded_face = {
                    "eventFolderPath": single_image_data['eventFolderPath'],
                    'ImageName': single_image_data['ImageName'],
                    "encoding": np.array(encoding),
                    'OrgId': single_image_data['OrgId'],
                    'EventId': single_image_data['EventId']
                            }
                nescessary_data.append(encoded_face)
    return nescessary_data

def event_encode_faces(data):
    event_encoded_faces = []
    for single_image_data in data:
        image = single_image_data['image']
        if image is not None:
            if "," in image:
                # Split the string at ','
                encoded_string = image.split(",")[1]
                encoded_face=event_encode_faces_preprocess(encoded_string,single_image_data)
                print(encoded_face, 'returned encoded_face:',len(encoded_face))
                event_encoded_faces.extend(encoded_face)
            else:
                encoded_string = image
                encoded_face=event_encode_faces_preprocess(encoded_string,single_image_data)
                # print(encoded_face, 'returned encoded_face:',len(encoded_face))
                event_encoded_faces.extend(encoded_face)
    print('total event_encoded_faces ',len(event_encoded_faces))
   
    return event_encoded_faces

def user_encode_faces_preprocess(encoded_string,oneuser):
    encoded_face=None
    oneimage = convert_Base64ToImgae(encoded_string)
    if oneimage is not None:
        # cv2.imshow('image', oneimage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        encodings = face_encoding(oneimage)
        # print("len of userencodingss", len(encodings))  # 1 1  1, 0 1 0
        if encodings:
            for encoding in encodings:
                encoded_face = {'UserId': oneuser["UserId"], "encoding": np.array(encoding)}
    return encoded_face

def user_encode_faces(one_user_face_encoded):
    users_encoded_faces = []
    if "image" in one_user_face_encoded and one_user_face_encoded["image"] is not None:
        for image in one_user_face_encoded["image"]:
            if image is not None:
                if "," in image:
                    # Split the string at ','
                    encoded_string = image.split(",")[1]
                    encoded_face=user_encode_faces_preprocess(encoded_string,one_user_face_encoded) 
                    users_encoded_faces.append(encoded_face)
                else:
                    encoded_string = image
                    encoded_face=user_encode_faces_preprocess(encoded_string,one_user_face_encoded) 
                    users_encoded_faces.append(encoded_face)
    return users_encoded_faces


def compare_faces(user_faces, tour_faces, threshold=0.5):
    similar_faces = []
    if user_faces is None or tour_faces is None:
        return similar_faces
    for user_face in user_faces:
        if user_face is None or "encoding" not in user_face:
            continue
        user_encoding = user_face["encoding"]
        for tour_face in tour_faces:
            if tour_face is None or "encoding" not in tour_face:
                continue
            tour_encoding = tour_face["encoding"]
            similarity_score = np.linalg.norm(user_encoding - tour_encoding, axis=0)
            # print(similarity_score)
            # similarity_score = cosine_similarity(user_encoding, tour_encoding)[0][0]
            if similarity_score < threshold:
                new_entry = {
                    "imagePath": tour_face['eventFolderPath'],
                    'imageName': tour_face['ImageName'],
                    'orgId': tour_face['OrgId'],
                    'userId': user_face['UserId'],
                    'eventId': tour_face['EventId']
                }
                similar_faces.append(new_entry)
    return similar_faces


def separate_unique_data(similar_tour_faces):
    unique_data = {}
    for item in similar_tour_faces:
        # Create a dictionary key using a unique combination of values from the data
        key = (item['imagePath'], item['imageName'],
               item['orgId'], item['userId'], item['eventId'])
        if key not in unique_data:
            unique_data[key] = item
    unique_data_list = list(unique_data.values())
    return unique_data_list
