import requests
import base64
from datetime import datetime
import json
import cv2
def convert_imgarrtobase64(img_arr):
    try:
        _,img_encoded=cv2.imencode('.jpg', img_arr)
        jpg_as_text=base64.b64encode(img_encoded).decode('utf-8')
        return jpg_as_text
    except:
        return None
def camera_run(id_bin,img, label):
    api='http://127.0.0.1:5000/post_data_cam'
    data={"id_bin": id_bin,
            "label": label
        }
    base64img=convert_imgarrtobase64(img)
    if base64img is not None:
        data['img']=base64img
        response=requests.post(api, json=data)
        print("Status code: ", response.status_code)
        print("Printing Entire Post Request")
        print(response.json())
    else:
        print("Status: failed")