import webapp2, jinja2, os, re
from google.appengine.ext import db
from models import Teacher, Student, Lesson

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class BlogHandler(webapp2.RequestHandler):

    def get_teachers(self):
        """ Get all posts ordered by *teacher (*alphabetical) """
        query = Teacher.all().order('teacher')
        return query.fetch() 

    def initialize(self, *a, **kw):
        """
            A filter to restrict access to certain pages when not logged in.
            If the request path is in the global auth_paths list, then the user
            must be signed in to access the path/resource.
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)

class IndexHandler(BlogHandler):

    def get(self):
        t = jinja_env.get_template("index.html")
        response = t.render() 
        self.response.write(response)

class LogLessonHandler(BlogHandler):


    def render_form(self, teacher="", student="", lessondate="",reason="", comment="", error=""):
        """ Render the new post form with or without an error, based on parameters """
        t = jinja_env.get_template("loglesson.html")
        teachers = Teacher.all()
        students = Student.all()
        response = t.render(teachers=teachers, students=students, lessondate=lessondate, reason=reason, comment=comment, error=error)
        self.response.out.write(response)


    def get(self):
        self.render_form()

    def post(self):
        """ Create a new post (lesson log) if possible. Otherwise, return with an error message """
        teacher = self.request.get("teacher")
        student = self.request.get("student")
        lessondate = self.request.get("lessondate")
        reason = self.request.get("reason")
        comment = self.request.get("comment")

        if teacher and student and lessondate and reason:

            # create a new Post object and store it in the database !!!!!!!!!!!!!!!
            loglesson = Teacher(
                teacher=teacher,
                student=student,
                lessondate=lessondate,
                reason = reason,
                comment = comment)
            loglesson.put()

            # get the id of the new post, so we can render the post's page (via the permalink)
            id = loglesson.key().id()
            self.redirect("/loglesson/%s" % id)
        else:
            error = "Please include a teacher, student, lesson date, reason and comment!"
            self.render_form(teacher, student, lessondate,reason, comment, error)

class CreateTeacherHandler(BlogHandler):

    def render_form(self, teacher="", temail="", tphone="", specialty="", error=""):
        """ Render the create teacher form with or without an error, based on parameters """
        t = jinja_env.get_template("createteacher.html")
        response = t.render(teacher=teacher, temail=temail, tphone=tphone, specialty=specialty, error=error)
        self.response.out.write(response)

    def get(self):
        self.render_form()

    def post(self):
        """ Create a new teacher if possible. Otherwise, return with an error message """
        teacher = self.request.get("teacher")
        temail = self.request.get("temail")
        tphone = self.request.get("tphone")
        specialty = self.request.get("specialty")

        if teacher and temail and tphone and specialty:

            #create a new teacher object and store it in the database
            teacher = Teacher(
                teacher=teacher,
                temail=temail,
                tphone=tphone, 
                specialty=specialty)
            teacher.put()

            id = teacher.key().id()
            self.redirect("/teacher/%s" % id)
        else:
            error = "Please include a teacher, an email, a phone number, and a specialty."
            self.render_form(teacher, temail, tphone, specialty, error)

class CreateStudentHandler(BlogHandler):

    def render_form(self, studentname="", semail="", sphone="", startdate="", error=""):
        """ Render the create student form with or without error, based on parameters """
        t = jinja_env.get_template("createstudent.html")
        response = t.render(student=student, semail=semail, sphone=sphone, startdate=startdate, error=error)
        self.response.out.write(response)

    def get(self):
        self.render_form()

    def post(self):
        """ Create a new student if possible, otherwise return an error """
        studentname = self.request.get("studentname")
        semail = self.request.get("semail")
        sphone = self.request.get("sphone")
        startdate = self.request.get("startdate")

        if studentname and semail and sphone and startdate: 

            #create new student object and store it in the database 
            student = Student(
                studentname=studentname, 
                semail=semail,
                sphone=sphone, 
                startdate=startdate)
            student.put()

            id = student.key().id()
            self.redirect("/student/%s" % id)
        else:
            error = "Please include name of student, an email, a phone number and a start date."
            self.render_form(studentname, semail, sphone, startdate, error)

class ViewTeachersHandler(BlogHandler): 

    def get(self):
        """ List all teachers  """
        teachers = Teacher.all().order('teacher')
        t = jinja_env.get_template("allteachers.html")
        response = t.render(teachers=teachers) 
        self.response.write(response)
    


class ViewStudentsHandler(BlogHandler):

    def get(self):
        """ List all students  """
        students = Student.all().order('student')
        t = jinja_env.get_template("allstudents.html")
        response = t.render(students=students) 
        self.response.write(response)

class LessonHandler(BlogHandler):

    def get(self, id):
        """Render page with lesson determined by the id(via the URL/permalink)"""

        lesson = Lesson.get_by_id(int(id))
        if lesson:
            t = jinja_env.get_template("lesson.html")
            response = t.render(lesson=lesson)
        else:
            error = "there is no lesson with id %s" % id
            t = jinja_env.get_template("404.html")
            response = t.render(error=error)

        self.response.out.write(response)


class TeacherHandler(BlogHandler):

    def get(self, id):
        """ Render a page with teacher determined by the id (via the URL/permalink) """

        teacher = Teacher.get_by_id(int(id))
        if teacher:
            t = jinja_env.get_template("teacher.html")
            response = t.render(teacher=teacher)
        else:
            error = "there is no teacher with id %s" % id
            t = jinja_env.get_template("404.html")
            response = t.render(error=error)

        self.response.out.write(response)

class StudentHandler(BlogHandler):

    def get(self, id):
        """ Render a page with teacher determined by the id (via the URL/permalink) """

        student = Student.get_by_id(int(id))
        if student:
            t = jinja_env.get_template("student.html")
            response = t.render(student=student)
        else:
            error = "there is no student with id %s" % id
            t = jinja_env.get_template("404.html")
            response = t.render(error=error)

        self.response.out.write(response)



app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/loglesson', LogLessonHandler),
    ('/createteacher', CreateTeacherHandler),
    ('/createstudent', CreateStudentHandler),
    webapp2.Route('/loglesson/<id:\d+>', LessonHandler),
    webapp2.Route('/teacher/<id:\d+>', TeacherHandler),
    webapp2.Route('/student/<id:\d+>', StudentHandler),
    ('/allteachers', ViewTeachersHandler),
    ('/allstudents', ViewStudentsHandler),
], debug=True)




#     ('/', IndexHandler),                -FROM BLOGZ-
#     ('/blog', BlogIndexHandler),
#     ('/blog/newpost', NewPostHandler),
#     webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
#     webapp2.Route('/blog/<username:[a-zA-Z0-9_-]{3,20}>', BlogIndexHandler),
# ], debug=True)


#                 <li><a href="/">Home</a></li>                  -FROM BASE.HTML-
#                 <li><a href="/createteacher">Create Teacher</a></li>
#                 <li><a href="/createstudent">Create Student</a></li>
#                 <li><a href="/loglesson">Log Lesson</a></li>
#                 <li><a href="/allteachers">Teachers</a></li> 
#                 <li><a href="/allstudents">Students</a></li>


# TODOS :

# - fix problem of duplicate entries for the same teachers/students
# - add status bar on student page for new student (boolean property/ if statement using startdate )
# - add individual lessons under student page 

