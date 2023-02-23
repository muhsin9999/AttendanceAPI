import face_recognition
from PIL import Image
import tempfile 
import cv2
import io


def find_encodings(image_data):
    # create a temporary file and write the binary data to it
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image_data)
        tmp.flush()

    img = cv2.imread(tmp.name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(img)[0]
    

    return face_encodings
        

def not_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        if not image.format:
            raise ValueError

    except Exception:
        return True
    return False