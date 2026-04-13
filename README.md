# Placement-Portal
This project is built using Flask, SQLAlchemy, HTML, CSS, and Bootstrap, and it is designed to manage the complete placement process between students, companies, and admin.

The system has three roles:

Admin
Company
Student

AUTHENTICATION:

In this portal:

Students and Companies can register themselves
Admin is pre-created in the database

Users can log in based on their role, and they are redirected to their respective dashboards.”

The Admin Dashboard shows:

Total Students
Total Companies
Total Placement Drives
Total Applications

Admin has full control over the system.

Admin can:

Approve or reject company registrations
Approve or reject placement drives
View all applications
Blacklist students or companies

Admin can also search:

Students by name, ID, or contact
Companies by name

This helps in easy management of large data.

Company can:

Complete their profile
Create placement drives (only after admin approval)
Edit or delete drives
Close drives

In the dashboard, the company can see:

All created drives
Number of applicants per drive

Now, let’s view applications.

Here, the company can:

See student details
View student resume
Update application status like:
Shortlisted
Selected
Rejected

This makes the hiring process very efficient.

Student can:

Register and login
Complete their profile
Upload resume

On the dashboard, student can see:

All approved placement drives
Drives they have applied to
Application status

Student can:

Apply to drives
View status updates
See placement history

Also, the system prevents:

Multiple applications to the same drive

“This project also includes important backend logic:

Only approved companies can create drives
Students can only see approved drives
Application status updates dynamically
Complete application history is maintained
Admin can access all historical data