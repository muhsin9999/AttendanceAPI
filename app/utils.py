from passlib.context import CryptContext
from fastapi import Response

import csv
import io


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def get_column_row(state, db, table, columns_to_exclude):
    if state == "all":
        column_names = [column.name for column in table.__table__.columns]
        rows = db.query(*[getattr(table, column_name) for column_name in column_names]).all()

    elif state == "exclude":
        columns_to_exclude = ['password', 'created_at']
        column_names = [column.name for column in table.__table__.columns if column.name not in columns_to_exclude]
        rows = db.query(*[getattr(table, column_name) for column_name in column_names]).all()

    return column_names, rows
        
        

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








