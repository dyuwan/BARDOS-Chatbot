import imutils
import cv2
from tensorflow import keras
import numpy as np

# parameters for loading data and images
detection_model_path = 'haarcascade_frontalface_default.xml'
emotion_model_path = '_mini_XCEPTION.102-0.66.hdf5'

# hyper-parameters for bounding boxes shape
# loading models


def output(img):

    image = cv2.imread(img)
    emotion_classifier = keras.models.load_model(emotion_model_path)
    EMOTIONS = ["angry", "disgust", "scared",
                "happy", "sad", "surprised", "neutral"]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
    roi = cv2.resize(gray, (64, 64))
    roi = roi.astype("float") / 255.0

    roi = keras.preprocessing.image.img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)

    preds = emotion_classifier.predict(roi)[0]
    label = EMOTIONS[np.argmax(preds)]

    if label == "happy" or label == "surprised" or label == "neutral":
        mood = "happy"
    elif label == "angry" or label == "disgust" or label == "scared" or label == "sad":
        mood = "sad"

    face_detection = cv2.CascadeClassifier(detection_model_path)
    faces = face_detection.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    faces = sorted(faces, reverse=True, key=lambda x: (
        x[2] - x[0]) * (x[3] - x[1]))[0]
    (x, y, w, h) = faces
    cv2.rectangle(image, (x - 2, y - 2),
                  (x + w + 4, y + h + 4), (0, 255, 0), 1)
    cv2.putText(image, label, (x - 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    return image, mood


# final, mood = output("D:\Downloads\screenshot.jpg")
# cv2.imshow("final", final)
# cv2.waitKey(0)
