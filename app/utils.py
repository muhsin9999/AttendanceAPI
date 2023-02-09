from passlib.context import CryptContext
from PIL import Image
import io

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def not_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        if not image.format:
            raise ValueError

    except Exception:
        return True

    return False


