import face_recognition
import io
import numpy as np
import cv2
import tempfile
from PIL import Image


def find_encodings(image_data):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image_data)
        tmp.flush()

    img = cv2.imread(tmp.name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(img)[0]
    
    return face_encodings
        

def is_not_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        if not image.format:
            raise ValueError
    except Exception:
        return True
    return False


async def process_image_files(files):
    face_encodings = []
    for file in files:
        contents = await file.read()
        if is_not_image(contents):
            return {"massage": "invalid image format"}

        face_encoding = find_encodings(contents)
        face_encodings.append(face_encoding)

    face_encodings = np.mean(face_encodings, axis=0)

    return face_encodings