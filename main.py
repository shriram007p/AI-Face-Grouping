from api import get_admin_ids, get_event_ids, get_event_and_user_image, post_data
from fg_auto_pipeline import event_encode_faces, user_encode_faces, compare_faces, separate_unique_data

def wholetrigger():
    postable_data=[]
    admin_ids = get_admin_ids()
    print(admin_ids)
    if admin_ids:
        for admin_id in admin_ids:
            event_ids = get_event_ids(admin_id)
            print(event_ids)
            if event_ids:
                for event_id in event_ids:

                    data = get_event_and_user_image(admin_id, event_id)
                    if data is not None:
        
                        #to call multiple events with multiple users
                        store_unique_data=new(data)
                        
                        postable_data.extend(store_unique_data)
                    else:
                        print("no data")
                    # try:
                    #     if data is not None:
                    #       print(data)
                    #       new(data)  # Assuming new is a function that could raise exceptions
                    # except Exception:
                    #     print("Error: nodata")
    print('the final data which is going for post',postable_data, 'length:',len(postable_data), type(postable_data)) #data comes in list format which postable
    #to post the all events all users unique data
    post_data(postable_data)

def new(data):
    one_event_multiuser=[]
    if data:
      
        event_face_encoded = event_encode_faces(data['EventImages'])
        print(len(event_face_encoded))
        # print(len(data['UserImages']))
        
     
        for one_user_face_encoded in data['UserImages']:
            user_face_encoded = user_encode_faces(one_user_face_encoded)

            similar_faces = compare_faces(user_face_encoded, event_face_encoded)
            unique_data = separate_unique_data(similar_faces)
            one_event_multiuser.extend(unique_data)

    return one_event_multiuser