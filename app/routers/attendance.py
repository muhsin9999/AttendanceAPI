from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import cv2
import face_recognition
from datetime import datetime, date

from app import models, oauth2
from app.database import get_db 

router = APIRouter(
    prefix="/attendance",
    tags=['Attendance'])




class AttendanceTaker:
    def __init__(self, db: Session, event: str, current_admin: dict, event_date: date):
        self.db = db
        self.event = event
        self.current_admin = current_admin
        self.event_date = event_date
        self.today_date = datetime.now().date()
        self.webcam = cv2.VideoCapture(0)
        self.staff_ids = []
        self.staff_names = []
        self.staff_known_encodings = []

    def mark_attendance(self, staff_id: int):
        if self.event_date != self.today_date:
            self.event_date = self.today_date
        today_attendance = self.db.query(models.Attendance, models.Staff).join(
            models.Attendance, 
            models.Staff.id == models.Attendance.staff_id).filter( 
                models.Attendance.event_date == self.event_date,
                models.Staff.admin_id == self.current_admin.id
        ).all()
        today_attendance = [obj[0].staff_id for obj in today_attendance if obj is not None]
        if staff_id not in today_attendance:
            attendee = models.Attendance(
                event=self.event, 
                staff_id=staff_id, 
                event_date=datetime.now().date(), 
                event_time=datetime.now().time()
            )
            self.db.add(attendee)
            self.db.commit()
            self.db.refresh(attendee)
        else:
            print("Attendance already recorded for this employee today.")

    def find_match(self, staff_known_encodings, face_encoding):
        matches = face_recognition.compare_faces(staff_known_encodings, face_encoding)
        face_distance = face_recognition.face_distance(staff_known_encodings, face_encoding)
        match_index = face_distance.argmin()

        return matches, match_index

    def analyze_frame(self, frame: cv2.VideoCapture):
        resized_frame = cv2.resize(frame, (0,0), None, 0.25, 0.25)
        resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        faces_cur_frame_locs = face_recognition.face_locations(resized_frame)
        face_encodings_cur_frame = face_recognition.face_encodings(resized_frame, faces_cur_frame_locs)
        faces_cur_frame_locs = [tuple(c * 4 for c in tup) for tup in faces_cur_frame_locs]
        return faces_cur_frame_locs, face_encodings_cur_frame 

    def get_attendance(self):
        staff_encoding_objs = self.db.query(models.Staff, models.FaceEncoding).join(
            models.FaceEncoding, 
            models.Staff.id == models.FaceEncoding.staff_id,
            isouter=True).filter(
                models.Staff.admin_id == self.current_admin.id
        ).all()
        try:
            self.staff_ids, self.staff_names, self.staff_known_encodings = zip(
                *[(obj[0].id, obj[0].name, obj[1].face_encoding) 
                    for
                    obj in staff_encoding_objs if obj[1] is not None]
            )
        except ValueError:
            print("No face encoding found for any staff member.")
        
        while True:
            success, frame = self.webcam.read()
            if not success:
                break
            faces_cur_frame_locs, faces_encodings_cur_frame = self.analyze_frame(frame)

            if faces_encodings_cur_frame != []:
                for face_location, face_encoding in zip(faces_cur_frame_locs, faces_encodings_cur_frame):
                    matches, match_index = self.find_match(self.staff_known_encodings, face_encoding)
                    
                    if matches[match_index]:
                        staff_id = self.staff_ids[match_index]
                        staff_name = self.staff_names[match_index]
                        self.mark_attendance(staff_id)
                        print(f"{staff_name} is marked present.")
                    else:
                        print("Unknown Person detected.")

            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.webcam.release()
        cv2.destroyAllWindows()


@router.post("/{event}/{event_date}")
async def take_attendance(
    event: str,
    event_date: date,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    attendance = AttendanceTaker(db, event, current_admin, event_date)

    attendance.get_attendance()
    




