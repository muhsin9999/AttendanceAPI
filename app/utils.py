from passlib.context import CryptContext
from fastapi import Response


from itertools import groupby
from datetime import date
import csv
import io

from app.face_rec import processimage


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)



def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




def download_file_csv(download_name, column_names, rows):
     # Write data to CSV file
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(column_names)
    for row in rows:
        writer.writerow(row)
    output.seek(0)

    # Return CSV file as response
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={download_name}.csv"
    return response


async def process_image_files(files):
    face_encodings = []
    for file in files:
        contents = await file.read()
        if processimage.not_image(contents):
            return {"massage": "invalid image format"}

        face_encoding = processimage.find_encodings(contents)
        face_encodings.append(face_encoding.tolist())

    return face_encodings







