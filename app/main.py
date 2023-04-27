from fastapi import FastAPI


from app import models
from app.routers import admin, staff, authentication, attendance
from .database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Attendance API")


app.include_router(admin.router)
app.include_router(staff.router)
app.include_router(authentication.router)
app.include_router(attendance.router)
