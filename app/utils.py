from passlib.context import CryptContext
import csv
import io


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def fetch_table_data(table, db, event_date, event, current_admin, columns_to_exclude=None):
    if columns_to_exclude:
        selected_columns = [getattr(table, column.name) for column in table.__table__.columns if column.name not in columns_to_exclude]
    else:
        selected_columns = [getattr(table, column.name) for column in table.__table__.columns] 
    rows = db.query(*selected_columns).filter(
        table.admin_id == current_admin,
        table.event_date == event_date,
        table.event == event
    ).all()
    print(rows)
    column_names = [column.name for column in table.__table__.columns if column in selected_columns]
    return column_names, rows
        
def write_file_csv(column_names, rows):
    output = io.StringIO()
    writer = csv.writer(output)
    column_names = [name.replace('_', ' ').title() for name in column_names]
    writer.writerow(column_names)
    for row in rows:
        writer.writerow(row)
    output.seek(0)

    return output









