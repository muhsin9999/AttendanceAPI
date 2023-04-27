from typing import List
import cv2
import face_recognition
from datetime import datetime, date
import io
import zipfile
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Response
from fastapi.responses import StreamingResponse
import logging

from app import models, utils


class AttendanceTaker:
    def __init__(self, db: Session, event: str, current_admin: dict, event_date: date = None):
        self.db = db
        self.event = event.capitalize()
        self.current_admin = current_admin
        self.event_date = event_date
        self.today_date = datetime.now().date()
        self.webcam = cv2.VideoCapture(0)
        self.staff_ids = []
        self.staff_names = []
        self.staff_known_encodings = []
        logging.basicConfig(
            level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def response(self, dates: List[datetime] = None):
        columns_to_exclude = ['id', 'event', 'created_at', 'admin_id']
        if dates is None:  # If no dates are provided, return a CSV file of attendance data for the event date
            column_names, rows = utils.fetch_table_data(
                table=models.Attendance, columns_to_exclude=columns_to_exclude,
                db=self.db, event_date=self.event_date, current_admin=self.current_admin.id, event=self.event
            )
            download_name = f"{self.event} Attendance({self.event_date})"
            return self.download_csv(column_names, rows, download_name)
        else:  # If dates are provided, return a ZIP file of attendance data for the specified dates
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as zip_archive:
                for date in dates:
                    column_names, rows = utils.fetch_table_data(
                        table=models.Attendance, columns_to_exclude=columns_to_exclude,
                        db=self.db, event_date=date, current_admin=self.current_admin.id, event=self.event
                    )

                    file_name = f"{self.event} Attendance({date})"
                    file_buffer = io.BytesIO()
                    file_contents = utils.generate_csv_output(
                        column_names, rows).getvalue().encode()
                    file_buffer.write(file_contents)
                    file_buffer.seek(0)

                    zip_archive.writestr(
                        f"{file_name}.csv", file_buffer.getvalue())

            buffer.seek(0)
            return self.download_zip(buffer)

    # returns a CSV file of attendance data
    def download_csv(self, column_names, rows, file_name):
        output = utils.generate_csv_output(column_names, rows)
        response = Response(content=output.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename={file_name}.csv"
        return response

    def download_zip(self, buffer):  # returns a ZIP file of attendance data
        response = StreamingResponse(
            buffer, media_type="application/octet-stream")
        response.headers["Content-Disposition"] = f"attachment; filename={self.event}.zip"
        response.headers["Content-Type"] = "application/octet-stream"
        return response

    def mark_attendance(self, staff_id: int):
        # Check if event date is not same as today's date to prevent db data manipulation
        if self.event_date != self.today_date:
            self.event_date = self.today_date

        # Query the database to get today's attendance for staff members to prevent double attendance
        today_attendance = self.db.query(models.Attendance, models.Staff).join(
            models.Attendance,
            models.Staff.id == models.Attendance.staff_id).filter(
                models.Attendance.event_date == self.event_date,
                models.Staff.admin_id == self.current_admin.id
        ).all()

        # Extract staff IDs that have already been marked as present
        today_attendance = [
            obj[0].staff_id for obj in today_attendance if obj is not None]

        is_marked_attendance = False
        if staff_id not in today_attendance:
            attendee_record = models.Attendance(
                event=self.event,
                staff_id=staff_id,
                event_date=datetime.now().date(),
                event_time=datetime.now().time(),
                admin_id=self.current_admin.id
            )
            self.db.add(attendee_record)
            self.db.commit()
            self.db.refresh(attendee_record)
            is_marked_attendance = True
        else:
            # Log a warning message if staff member is already marked as present
            logging.warning('Attendance already recorded today.')

        return is_marked_attendance

    def draw_face_box_with_text(self, face_location, text, frame, text_colour, box_colour):
        # Draw a rectangle around the face with text indicating the staff member's name
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom),
                      box_colour, thickness=2)
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), box_colour, cv2.FILLED)
        cv2.putText(frame, text, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_COMPLEX, 1, text_colour, thickness=2)

    def find_match(self, staff_known_encodings, face_encoding):
        matches = face_recognition.compare_faces(
            staff_known_encodings, face_encoding)
        face_distance = face_recognition.face_distance(
            staff_known_encodings, face_encoding)
        match_index = face_distance.argmin()

        return matches, match_index

    def analyze_frame(self, frame: cv2.VideoCapture):
        # Resize the current frame and convert it to RGB format
        resized_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces in the current frame and their corresponding encoding and face locations
        faces_cur_frame_locs = face_recognition.face_locations(resized_frame)
        face_encodings_cur_frame = face_recognition.face_encodings(
            resized_frame, faces_cur_frame_locs)
        faces_cur_frame_locs = [tuple(c * 4 for c in tup)
                                for tup in faces_cur_frame_locs]

        return faces_cur_frame_locs, face_encodings_cur_frame

    def get_attendance(self):
        # Query the database to get all staff members and their face encodings
        staff_encoding_objs = self.db.query(models.Staff, models.FaceEncoding).join(
            models.FaceEncoding,
            models.Staff.id == models.FaceEncoding.staff_id,
            isouter=True).filter(
                models.Staff.admin_id == self.current_admin.id
        ).all()

        # Unzip the results to get separate lists of staff ids, names, and known encodings
        try:
            self.staff_ids, self.staff_names, self.staff_known_encodings = zip(
                *[(obj[0].id, obj[0].name, obj[1].face_encoding)
                    for
                    obj in staff_encoding_objs if obj[1] is not None]
            )
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No face encoding found for any staff member.")

        while True:
            success, frame = self.webcam.read()
            if not success:
                break
            faces_cur_frame_locs, faces_encodings_cur_frame = self.analyze_frame(
                frame)

            if faces_encodings_cur_frame != []:
                for face_location, face_encoding in zip(faces_cur_frame_locs, faces_encodings_cur_frame):
                    matches, match_index = self.find_match(
                        self.staff_known_encodings, face_encoding)

                    if matches[match_index]:
                        staff_id = self.staff_ids[match_index]
                        staff_name = self.staff_names[match_index]
                        self.draw_face_box_with_text(
                            face_location, staff_name, frame,
                            text_colour=(255, 255, 255), box_colour=(0, 255, 0)
                        )

                        is_marked_attendance = self.mark_attendance(staff_id)
                        if is_marked_attendance:
                            logging.info(
                                'f{staff_name} attendance marked successfully')
                    else:
                        logging.info("Unknown person detected at {time}".format(
                            time=datetime.now()))

            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.webcam.release()
        cv2.destroyAllWindows()
        return self.response()

    def delete_attendance(self):
        record = self.db.query(
            models.Attendance).filter(
            models.Attendance.event == self.event,
            models.Attendance.event_date == self.event_date,
            models.Attendance.admin_id == self.current_admin.id
        )
        if not record.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance with date: {date} or Event Name {self.event} does not exist"
            )
        record.delete(synchronize_session=False)
        self.db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
