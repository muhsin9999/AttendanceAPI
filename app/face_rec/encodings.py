import face_recognition
import tempfile 
import cv2
import numpy as np



def detect_faces(frame):
    face_locations = face_recognition.face_locations(frame)

    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    
    cv2.putText(frame, "Press 'c' to take a capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
   

def capture_encoding(frame):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        cv2.imwrite(tmp.name, frame)
        tmp.flush()

    img = cv2.imread(tmp.name)
    face_encoding = face_recognition.face_encodings(img)[0]
    cv2.putText(frame, "Capture Taken", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    return face_encoding


def cam_capture():
    face_encodings = []
    webcam = cv2.VideoCapture(0)

    num_captures = 0

    while True:

        success, frame = webcam.read()

        if not success:
            print('Failed to grab frame')
            break

        detect_faces(frame)

        if num_captures > 4:
            break

        key = cv2.waitKey(1)


        if key == ord('c'): 
            resized_img = cv2.resize(frame, (0,0), None, 0.25, 0.25)
            resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

            face_encoding = capture_encoding(resized_img)

            face_encodings.append(face_encoding)
            cv2.putText(frame, "Capture Taken", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
            print(num_captures)
            num_captures += 1


        elif key == ord('q'):
            print("Turning off camera.")
            break
        
        # Show the current frame
        cv2.imshow("Capturing", frame)
        

    webcam.release()
    cv2.destroyAllWindows()


    if len(face_encodings) == 5:
        face_encodings = np.mean(face_encodings, axis=0)
        return face_encodings  













        

