import base64
import cv2
import numpy as np


def convert_Base64ToImgae(base64_string):
    try:
        # Decode the base64 string into bytes
        image_byte_data = base64.b64decode(base64_string)

        # Convert the bytes to a numpy array
        nparr = np.frombuffer(image_byte_data, np.uint8)

        if len(nparr) != 0:
            # Decode the numpy array as an image
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is not None:
                return image
            else:
                print("Error: Unable to decode image.")
                return None
        else:
            print("Error: Empty numpy array.")
            return None
    except Exception as e:
        print(f"Error:")
        return None
