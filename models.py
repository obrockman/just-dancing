from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Teacher(polymodel.PolyModel):
    teacher = db.StringProperty()
    temail = db.StringProperty()
    tphone = db.StringProperty()
    specialty = db.StringProperty()

class Student(Teacher):
    student = db.StringProperty()
    semail = db.StringProperty()
    sphone = db.StringProperty()
    startdate = db.StringProperty()

class Lesson(Teacher):
    lessondate = db.StringProperty()
    reason = db.StringProperty()
    comment = db.TextProperty()


    

   