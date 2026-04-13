from flask import Flask , redirect ,render_template , request ,url_for ,flash
from flask import current_app as app
from .models import *
import os

@app.route("/" , methods=["GET" ,"POST"])
def login():
    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        this_user = User.query.filter_by(email =email).first()
        if this_user:
            if this_user.password == password:
                if this_user.is_blacklisted == "NO":
                    if this_user.role == "HR":
                        return redirect(f"/company_dashboard/{this_user.id}")
                    elif this_user.role == "Student":
                        return redirect(f"/student_dashboard/{this_user.id}")
                    elif this_user.role == "admin":
                        return redirect("admin_dashboard")
                else:
                    return "<h1> You are Blacklisted Contact Admin </h1>"
            else:
                return "<h1> Incorrect Password </h1>"
        else:
            return "<h1> User does Not Exists </h1> "
    return render_template("login.html")


@app.route("/register" , methods=["GET" , "POST"])
def register():
    if request.method == "POST":
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        username = request.form.get("username")
        contact = request.form.get("contact")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return "Email already taken"
        existing_contact = User.query.filter_by(contact=contact).first()
        if existing_contact:
            return "Contact number already taken"
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return "Username already taken"
        new_user = User(f_name = f_name , l_name = l_name , username = username , contact =contact , email =email , password = password , role = role)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/")
    return render_template("/register.html")

@app.route("/admin_dashboard")
def ad_dashboard():
    all_students = User.query.filter_by(role = "Student").all()
    all_company = Company.query.filter_by(status = "Approved").all()
    drives = Drive.query.filter_by(status="Pending").all()
    approve_drive = Drive.query.filter_by(status = "Approved").all()
    total_companies = len(all_company)
    total_students = len(all_students)
    total_drives = len(approve_drive)
    total_applications = Application.query.count()
    pending_count = len(drives)
    return render_template("admin_dashboard.html" , drives =drives , pending_count =pending_count ,all_students = all_students ,  all_company = all_company , total_applications =total_applications , total_companies =total_companies, total_drives =total_drives , total_students =total_students)

@app.route("/admin_search")
def admin_search():
    student_search = request.args.get("student_search")
    company_search = request.args.get("company_search")
    searched_students = []
    if student_search:
        if student_search.isdigit():
            student = User.query.filter_by(id=int(student_search)).all()
            searched_students.extend(student)
        students_name = User.query.filter(User.f_name.ilike(f"%{student_search}%")).all()
        students_lname = User.query.filter(User.l_name.ilike(f"%{student_search}%")).all()
        students_contact = User.query.filter(User.contact.ilike(f"%{student_search}%")).all()
        full_name_students = User.query.filter((User.f_name + " " + User.l_name).ilike(f"%{student_search}%")).all()
        searched_students = list({ s.id: s for s in ( searched_students + students_name + students_lname + students_contact + full_name_students)}.values())
    searched_company = []
    if company_search:
        searched_company = Company.query.filter(Company.company_name.ilike(f"%{company_search}%")).all()
    return render_template("admin_dashboard.html",all_students=searched_students,all_company=searched_company )
@app.route("/admin_comp_approve")
def comp_approve():
    all_company = Company.query.filter_by(status = "Pending").all()
    return render_template("admin_comp_approve.html", all_company = all_company )

@app.route("/admin_stud_approve")
def stud_approve():
    all_application = Application.query.filter_by().all()
    return render_template("admin_stud_approve.html" , all_application =all_application)

@app.route("/admin_on_drive")
def on_drive():
    all_drives = Drive.query.filter_by().all()
    all_company = Company.query.filter_by().all()
    return render_template("admin_on_drive.html" , all_drives = all_drives , all_company =all_company)

@app.route("/approve_company/<int:company_id>")
def approve_comp(company_id):
    this_company = Company.query.filter_by(id = company_id).first()
    this_company.status = "Approved"
    db.session.commit()
    return redirect("/admin_comp_approve")

@app.route("/reject_company/<int:company_id>")
def reject_comp(company_id):
    this_company = Company.query.filter_by(id = company_id).first()
    this_company.status = "Rejected"
    db.session.commit()
    return redirect("/admin_comp_approve")


@app.route("/blacklist/<int:user_id>")
def blacklist(user_id):
    user = User.query.filter_by(id =user_id).first()
    if user:
        if user.is_blacklisted == "NO":
            user.is_blacklisted = "YES"
        else:
            user.is_blacklisted = "NO"
        db.session.commit()
    return redirect("/admin_dashboard")

@app.route("/admin_view_drive/<int:drive_id>")
def view_drive(drive_id):
    this_drive= Drive.query.filter_by( id = drive_id).first()
    return render_template("admin_view_drive.html" , this_drive =this_drive)

@app.route("/admin_view_student_application/<int:student_id>/<int:drive_id>")
def view_student_application(student_id , drive_id):
    this_student =  Student.query.filter_by(student_id =student_id).first()
    this_drive = Drive.query.filter_by(id = drive_id).first()
    return render_template("admin_view_student_app.html" , this_student =this_student , this_drive =  this_drive)

@app.route("/admin_drive_status/<int:drive_id>")
def drive_status(drive_id):
    this_drive = Drive.query.filter_by(id =drive_id).first()
    this_drive.status = "Completed"
    db.session.commit()
    return redirect("/admin_on_drive")

@app.route("/admin_drive_approve/<int:drive_id>")
def approve_drive(drive_id):
    this_drive = Drive.query.get(drive_id)
    this_drive.status = "Approved"
    db.session.commit()
    return redirect("/admin_dashboard")

@app.route("/admin_drive_reject/<int:drive_id>")
def reject_drive(drive_id):
    this_drive = Drive.query.get(drive_id)
    this_drive.status = "Reject"
    db.session.commit()
    return redirect("/admin_dashboard")

@app.route("/delete_company/<int:user_id>")
def delete_comp(user_id):
    company = Company.query.filter_by(company_id=user_id).first()
    if company:
        drives = Drive.query.filter_by(company_id=company.company_id).all()
        for drive in drives:
            placements = Placement.query.filter_by(drive_id=drive.id).all()
            for place in placements:
                db.session.delete(place)
            apps = Application.query.filter_by(drive_id=drive.id).all()
            for app in apps:
                db.session.delete(app)
            db.session.delete(drive)

        db.session.delete(company)
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect("/admin_dashboard")

@app.route("/delete_student/<int:user_id>")
def delete_user(user_id):
    student = Student.query.filter_by(student_id=user_id).first()
    if student:
        placements = Placement.query.filter_by(student_id=student.id).all()
        for place in placements:
            db.session.delete(place)
        apps = Application.query.filter_by(student_id=student.student_id).all()
        for application in apps:
            db.session.delete(application)
        db.session.delete(student)

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect("/admin_dashboard")
    













@app.route("/student_dashboard/<int:user_id>") 
def student_dashboard(user_id):
    this_user = User.query.filter_by(id = user_id).first()
    all_company = Company.query.filter().all()
    all_application = Application.query.filter_by(status = "Applied").all()

    return render_template("student_dashboard.html" , this_user = this_user , all_company =all_company , all_application =all_application)

@app.route("/view_company/<int:company_id>/<int:user_id>")
def view_company(company_id , user_id):
    this_student = Student.query.filter_by(student_id = user_id).first()
    all_drives = Drive.query.filter_by(company_id =company_id).all()
    this_company = Company.query.filter_by(company_id = company_id).first()
    return render_template("stu_view_company.html" , all_drives = all_drives , this_company =this_company , user_id =user_id , this_student = this_student)

@app.route("/stu_drive/<int:drive_id>/<int:company_id>/<int:user_id>")
def stu_drive(drive_id , company_id ,user_id):
    this_drive = Drive.query.filter_by(id = drive_id).first()
    this_company = Company.query.filter_by(company_id = company_id).first()
    return render_template("stu_drive_apply.html" , this_drive = this_drive , this_company =this_company , user_id =user_id)

@app.route("/stu_application/<int:drive_id>/<int:company_id>/<int:user_id>")
def stu_application(drive_id ,company_id , user_id):
    this_user = User.query.filter_by(id = user_id).first()
    if this_user.profile_status == "Pending":
        return ("First Complete Your Profile!")
    existing = Application.query.filter_by(student_id = user_id , drive_id = drive_id ,company_id = company_id).first()
    if existing:
        return("You have already applied for this company in this drive!")
    this_application = Application(drive_id =drive_id , company_id =company_id ,student_id =user_id , user_id =user_id)
    db.session.add(this_application)
    db.session.commit()
    return redirect(f"/student_dashboard/{user_id}")

@app.route("/student_application_history/<int:student_id>")
def stu_application_history(student_id):
    this_user = User.query.get(student_id)
    this_student = Student.query.filter_by(student_id =student_id).first()
    all_application = Application.query.filter_by(student_id= student_id).all()
    return render_template("student_application_history.html" , all_application=all_application ,this_user =this_user , this_student =this_student)






@app.route("/edit_stu_profile/<int:user_id>", methods=["GET" ,"POST"])
def edit_stu_profile(user_id):
    this_user = User.query.filter_by(id = user_id).first()
    if request.method == "POST":
        this_user.profile_status = "Completed"
        this_user.f_name = request.form.get("f_name")
        this_user.l_name = request.form.get("l_name")
        dept = request.form.get("dept")
        skills = request.form.get("skills")
        city = request.form.get("city")
        file = request.files.get("resume")
        filename = None
        if file and file.filename != "":
           if file.filename.endswith(".pdf"):
            filename = str(user_id) + "_resume.pdf"
            filepath = os.path.join("static/resumes", filename)
            file.save(filepath)
        student = Student.query.filter_by(student_id=user_id).first()
        if student:
            student.dept = dept
            student.skills = skills
            student.city = city
            if filename:  
                student.resume = filename
        else:
            student = Student(dept=dept,skills=skills,city=city,student_id=this_user.id,resume=filename if filename else "")
        db.session.add(student)
        db.session.commit()
        return redirect(f"/student_dashboard/{this_user.id}")
    return render_template("edit_stu_profile.html" , this_user=this_user)

@app.route("/company_dashboard/<int:user_id>")
def company_dashboard(user_id):
    placed_students = Placement.query.filter_by().all()
    ongoing_all_drives = Drive.query.filter_by(company_id = user_id , status = "Approved").all()
    total_ongoing_drives = len(ongoing_all_drives)
    completed_drives = Drive.query.filter_by(company_id = user_id , status = "Completed").all()
    rejected_drives = Drive.query.filter_by(company_id = user_id , status = "Reject").all()
    pending_drives = Drive.query.filter_by(company_id = user_id , status = "Pending").all()
    t_pending_drive = len(pending_drives)
    t_rejected_drive = len(rejected_drives)
    t_completed_drive = len(completed_drives)
    company_profile = Company.query.filter_by(company_id = user_id).first()
    this_user = User.query.filter_by(id = user_id).first()
    

    return render_template("company_dashboard.html" , placed_students = placed_students ,this_user = this_user , company_profile = company_profile , ongoing_all_drives = ongoing_all_drives , total_ongoing_drives =total_ongoing_drives , completed_drives = completed_drives , rejected_drives =rejected_drives , t_completed_drive =t_completed_drive , t_rejected_drive = t_rejected_drive , pending_drives =pending_drives , t_pending_drive = t_pending_drive )

@app.route("/edit_comp_profile/<int:user_id>" , methods = ["GET" , "POST"])
def edit_comp_profile(user_id):
    this_user = User.query.filter_by(id = user_id).first()
    company_profile = Company.query.filter_by(company_id = user_id)
    if request.method == "POST":
        this_user.profile_status = "Completed"
        company_name = request.form.get("company_name")
        website = request.form.get("website")
        hr_contact = request.form.get("hr_contact")
        city = request.form.get("city")
        year = request.form.get("year")
        complete_profile = Company( company_id = this_user.id , company_name = company_name , website = website , hr_contact = hr_contact , city =city ,year =year)
        db.session.add(complete_profile)
        db.session.commit()
        return redirect(f"/company_dashboard/{this_user.id}")
    if request.method == "GET":
        if this_user.profile_status == "Completed":
            return ("You Are Already Completed Your Profile!!")
        else:
            return render_template("edit_comp_profile.html" , this_user =this_user , company_profile = company_profile)

    

@app.route("/create_drive/<int:user_id>" ,methods = ["GET" , "POST"])
def create_drive(user_id):
    this_comp = Company.query.filter_by(company_id = user_id).first()
    this_user = User.query.filter_by(id = user_id).first()
    if request.method== "POST":
        if this_comp.status =="Approved":
            job_title = request.form.get("job_title")
            job_description = request.form.get("job_desc")
            min_cgpa = request.form.get("min_cgpa")
            drive_name = request.form.get("drive_name")
            salary = request.form.get("salary")
            new_drive = Drive( company_id = this_comp.company_id ,job_title = job_title , job_description = job_description , min_cgpa =min_cgpa , drive_name =drive_name , salary =salary)
            db.session.add(new_drive)
            db.session.commit()
            return redirect(f"/company_dashboard/{this_comp.company_id}")
        else:
            return ("Sorry You Are Not Approved by Admin!!")
    if request.method == "GET":
        if this_user.profile_status == "Completed" and this_comp.status == "Approved":
            return render_template("create_drive.html" , this_comp =this_comp)
        
        else:
            return ("Complete Your Profile First Or You are Still Not Approved By Admin!!")
        
        

@app.route("/company_drive_completed/<int:drive_id>")
def comp_drive_completed(drive_id):
    this_drive = Drive.query.filter_by(id =drive_id).first()
    this_drive.status = "Completed"
    db.session.commit()
    return redirect(f"/company_dashboard/{this_drive.company_id}")

@app.route("/company_drive_status/<int:drive_id>")
def comp_update_drive_status(drive_id):
    this_drive = Drive.query.filter_by(id =drive_id).first()
    this_drive.status = "Pending"
    db.session.commit()
    return redirect(f"/company_dashboard/{this_drive.company_id}")

@app.route("/company_delete_drive/<int:drive_id>")
def delete_drive(drive_id):
    this_drive = Drive.query.get(drive_id)
    db.session.delete(this_drive)
    db.session.commit()
    return redirect(f"/company_dashboard/{this_drive.company_id}")

@app.route("/company_view_detail/<int:drive_id>")
def student_det(drive_id):
    this_drive = Drive.query.get(drive_id)
    all_applications = Application.query.filter_by(drive_id = drive_id).all()

    return render_template("company_view_detail.html" , this_drive =this_drive , all_applications =all_applications)

@app.route("/company_review_application/<int:application_id>")
def review_application(application_id):
    this_application = Application.query.get(application_id)
    return render_template("/company_review_stu_app.html", this_application = this_application)

@app.route("/update_student_application/<int:application_id>" , methods = ["GET" , "POST"])
def update_application(application_id):
    this_application = Application.query.get(application_id)
    if request.method =="POST":
        new_status = request.form.get("status")
        if new_status == "Placed":
            placed_id = this_application.student_id 
            placed_drive_id = this_application.drive.id
            placement = Placement(student_id = placed_id , drive_id = placed_drive_id)
            db.session.add(placement)
            this_application.status = new_status
            db.session.commit()
        else:
            this_application.status = new_status
            db.session.commit()
        return redirect(f"/company_view_detail/{this_application.drive.id}")
    




