import cv2
import os
import numpy as np
from PIL import Image
import requests


if not os.path.exists("haarcascade.xml"):
    print("Downloading face detector...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    r = requests.get(url)
    with open("haarcascade.xml", "wb") as f:
        f.write(r.content)

face_detector = cv2.CascadeClassifier("haarcascade.xml")

# create folders
os.makedirs("dataset", exist_ok=True)
os.makedirs("trainer", exist_ok=True)


def open_camera():
    for index in range(3):  # try 0,1,2
        cam = cv2.VideoCapture(index)
        if cam.isOpened():
            print(f"Camera opened successfully (Index {index})")
            return cam
    print("ERROR: Could not access camera.")
    return None


def register_face():
    cam = open_camera()
    if cam is None:
        return

    user_id = input("Enter your ID number (1,2,3...): ")
    print("Look at camera. Collecting samples...")

    count = 0

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            face_img = gray[y:y+h, x:x+w]
            count += 1

            cv2.imwrite(f"dataset/User.{user_id}.{count}.jpg", face_img)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imshow("Register Face", img)

        if cv2.waitKey(1)==27 or count>=15:
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Face Registered Successfully!")

# ---------------------------
# TRAIN MODEL (FAST)
# ---------------------------
def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    ids = []

    print("Training...")

    for file in os.listdir("dataset"):
        path = os.path.join("dataset", file)
        img = Image.open(path).convert('L')
        img_np = np.array(img, 'uint8')

        id = int(file.split(".")[1])

        faces.append(img_np)
        ids.append(id)

    if len(faces)==0:
        print("No dataset found. Register first.")
        return

    recognizer.train(faces, np.array(ids))
    recognizer.write("trainer/trainer.yml")

    print("Training Completed!")

# ---------------------------
# RECOGNIZE FACE
# ---------------------------
def recognize_face():

    if not os.path.exists("trainer/trainer.yml"):
        print("Train the model first!")
        return

    cam = open_camera()
    if cam is None:
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer/trainer.yml")

    print("Press ESC to exit")

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 3)

        for (x,y,w,h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            if confidence < 65:
                text = f"Person {id}"
                color = (0,255,0)
            else:
                text = "Unknown"
                color = (0,0,255)

            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img,text,(x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)

        cv2.imshow("Face Recognition", img)

        if cv2.waitKey(1)==27:
            break

    cam.release()
    cv2.destroyAllWindows()

# ---------------------------
# MENU
# ---------------------------
while True:
    print("\n===== FACE AI SYSTEM =====")
    print("1. Register Face")
    print("2. Train Model")
    print("3. Recognize Face")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice=='1':
        register_face()

    elif choice=='2':
        train_model()

    elif choice=='3':
        recognize_face()

    elif choice=='4':
        break

    else:
        print("Invalid choice")