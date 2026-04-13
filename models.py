from .database import db
from datetime import date


class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    f_name = db.Column(db.String(20) , nullable = False)
    l_name = db.Column(db.String(20) , nullable = False)
    username = db.Column(db.String() , nullable = False , unique = True)
    email = db.Column(db.String() , nullable = False ,  unique = True )
    contact =db.Column(db.String() , nullable = False , unique = True)
    password = db.Column(db.String(), nullable = False)
    role = db.Column(db.String(), nullable = False)
    is_blacklisted = db.Column(db.String() , nullable = False ,default = "NO")
    profile_status = db.Column(db.String() , nullable = False , default = "Pending")

class Student(db.Model):
    id = db.Column(db.Integer , primary_key =True)
    student_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    dept = db.Column(db.String() , nullable = False )
    city = db.Column(db.String() , nullable = False)
    skills = db.Column(db.String() , nullable = False)
    resume = db.Column(db.String() , nullable = False)
    user = db.relationship("User" , backref = "student_profile")


class Company(db.Model):
    id = db.Column(db.Integer , primary_key =True)
    company_id = db.Column(db.Integer , db.ForeignKey("user.id" , ondelete="CASCADE") , nullable = False , unique = True )
    company_name = db.Column(db.String() , nullable = False)
    status = db.Column(db.String , default = "Pending")
    website = db.Column(db.String() , nullable = False)
    hr_contact = db.Column(db.String() , nullable = False)
    city = db.Column(db.String() , nullable = False)
    year = db.Column(db.String() , nullable = False)
    user = db.relationship("User" , backref = "company_profile") 


class Drive(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer , db.ForeignKey("company.company_id") , nullable = False)
    drive_name = db.Column(db.String() , nullable =  False)
    job_title = db.Column(db.String() , nullable = False)
    job_description = db.Column(db.String() , nullable = False)
    min_cgpa = db.Column(db.Float() , nullable = False)
    salary = db.Column(db.String() , nullable = False)
    status = db.Column(db.String() , nullable = False , default = "Pending")
    company = db.relationship("Company", backref = "drive")


class Application(db.Model):
    application_id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id") , nullable = False)
    company_id = db.Column(db.Integer , db.ForeignKey("company.company_id") , nullable = False)
    student_id = db.Column(db.Integer , db.ForeignKey("student.student_id") , nullable = False)
    drive_id = db.Column(db.Integer ,  db.ForeignKey("drive.id") , nullable = False)
    application_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String() , nullable = False , default= "Applied")
    company = db.relationship("Company" , backref = "application")
    student = db.relationship("Student" , backref = "application")
    drive = db.relationship("Drive",  backref ="application")
    user = db.relationship("User",  backref ="application")

class Placement(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    student_id = db.Column(db.Integer , db.ForeignKey("student.id") , nullable = False)
    drive_id = db.Column(db.Integer , db.ForeignKey("drive.id") , nullable = False)
    placed_date = db.Column(db.Date , default = date.today)
    student = db.relationship("Student" , backref = "placement")
    drive = db.relationship("Drive" , backref = "placement")
    


    
    




