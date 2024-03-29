import joblib
import json
import numpy as np
import base64
import cv2
from Wavelet import waveletTrans
import os

__class_name_to_number ={}
__class_number_to_name={}

__model = None

def classify_image(image_base64_data,file_path=None):
    images=get_cropped_image_if_2_eyes(file_path,image_base64_data)

    result=[]
    
    for img in images:
        scalled_raw_img = cv2.resize(img, (48, 48))
        img_har = waveletTrans(scalled_raw_img, "db1", 5)
        #         scalled_img_har=cv2.resize(img_har,(48,48))
        combined_image = np.vstack((scalled_raw_img.reshape(48 * 48 * 3, 1), img_har.reshape(48 * 48, 1)))

        len_image_array=48*48*3+48*48

        final=combined_image.reshape(1,len_image_array).astype(float)

        # result.append(class_number_to_name(__model.predict(final)[0]))

        ''' Buat ngecek hasil prediksi
        print(__model.predict(final))
        print(__model.predict(final)[0])
        '''
        # result=[{
        #     "class":class_number_to_name(__model.predict(final)[0]),
        #     "class_probability":np.round(__model.predict_proba(final)*100,2).tolist()[0],
        #     "class_dictionary":__class_name_to_number
        # }]
        
        result.append({
            "class":class_number_to_name(__model.predict(final)[0]),
            "class_probability":np.round(__model.predict_proba(final)*100,2).tolist()[0],
            "class_dictionary":__class_name_to_number
        })

        # print(result[0]["class"])
        # __model.predict_proba(final)
    return result

def load_saved_artifacts():
    print("Loading saved artifacts...\nStart")
    global __class_name_to_number
    global __class_number_to_name

    with open(os.path.dirname(os.path.abspath(__file__))+"/Artifacts/Class_dictionary.json","r") as f:
        __class_name_to_number=json.load(f)
        __class_number_to_name={v:k for k,v in __class_name_to_number.items()}

    global __model
    if __model is None:
        with open(os.path.dirname(os.path.abspath(__file__))+"/Artifacts/Saved_Model.pkl","rb") as f:
            __model=joblib.load(f)
    print("Loading saved artifacts...\nDone")

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

def get_cv2_image_from_base64_string(base64str):
    '''
    credit: https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    :param base64str:
    :return:
    '''

    encoded_data = base64str.split(",")[1]
    nparr=np.frombuffer(base64.b64decode(encoded_data),np.uint8)
    img=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    return img


def get_cropped_image_if_2_eyes(image_path,image_base64_data):
    face_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.abspath(__file__))+"/opencv/haarcascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.abspath(__file__))+"/opencv/haarcascades/haarcascade_eye.xml")

    if image_path:
        img=cv2.imread(image_path)
    else:
        img=get_cv2_image_from_base64_string(image_base64_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
    return cropped_faces


def getBase64_testImage_for_jackMa():
    with open("base64.txt") as f:
        return f.read()

if __name__=="__main__":
    load_saved_artifacts()
    # print(classify_image(getBase64_testImage_for_jackMa(), None))
    # print(classify_image(None,"./test_image/Image_1.jpg"))
    print(os.path.dirname(os.path.abspath(__file__))+"\\test_image\\test.jpg")
    print(classify_image(None, "D:\GitHub\Billionaires_Image-Classification\Website UI\\test_image\\test.jpg"))
    # print(classify_image(None, "./test_image/Image_3.jpg"))
    # print(classify_image(None, "./test_image/Image_21.jpg"))
    # print(classify_image(None, "./test_image/Image_23.jpg"))
    # print(classify_image(None, "./test_image/Image_22.jpg"))
    # print(classify_image(None, "./test_image/Image_11.jpeg"))
