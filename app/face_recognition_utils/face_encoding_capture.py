import cv2
import face_recognition
import numpy as np
import tempfile


def detect_and_draw_faces(frame):
    # Use face_recognition library to locate faces in the frame
    face_locations = face_recognition.face_locations(frame)

    # Draw rectangles around each detected face
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 1)

    # Return whether any faces were found in the frame
    return len(face_locations) > 0


def capture_face_encoding(frame):
    # Create temporary file to store image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        cv2.imwrite(tmp.name, frame)
        tmp.flush()

    # Write frame to file
    img = cv2.imread(tmp.name)
    
    face_encoding = face_recognition.face_encodings(img)[0]
    cv2.putText(frame, "Capture Taken", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return face_encoding


def capture_multiple_face_encodings(num_captures=5):
    face_encodings = []
    webcam = cv2.VideoCapture(0)
    captures_remaining = num_captures

    while True:
        success, frame = webcam.read()

        if not success:
            break

        found_face = detect_and_draw_faces(frame)

        if captures_remaining == 0:
            break

        key_press = cv2.waitKey(1)

        if key_press == ord('c'):
            # Resize frame to 1/4 size for faster processing
            resized_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)

            # Convert color from BGR (OpenCV default) to RGB (face_recognition library default)
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

            if found_face:
                face_encoding = capture_face_encoding(resized_frame)

                face_encodings.append(face_encoding)
                cv2.putText(frame, "Capture Taken", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                captures_remaining -= 1

        elif key_press == ord('q'):
            break

        cv2.putText(frame, "Press 'c' to take a capture", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Capturing", frame)

    webcam.release()
    cv2.destroyAllWindows()

    if len(face_encodings) == num_captures:
        mean_face_encodings = np.mean(face_encodings, axis=0)
        return mean_face_encodings
    else:
        return None









