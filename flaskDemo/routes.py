import os
import secrets
import numpy as np
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskDemo.models import User, Books, Inventory, Borrower_Copies, Borrower
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')



# *** approute to list employee assigned to a project
#@app.route("/employee_assigned")
#@login_required
#def employee_assigned():
#    results2 = Works_On.query.join(Employee,Works_On.essn == Employee.ssn) \
#                .add_columns(Employee.fname, Employee.lname, Works_On.essn, Works_On.pno) \
#                .join(Project, Works_On.pno == Project.pnumber) \
#                .add_columns(Project.pname) \
#                .order_by(Employee.fname.asc())
#    return render_template('employee_assigned.html', title='Employee Assigned', joined_m_n=results2)


# *** route to assign employee to project
#@app.route("/assign", methods=['GET', 'POST'])
#@login_required
#def assign():
#    form = AssignToProject()
#    if form.validate_on_submit():
#        employeProject = Works_On(essn=form.essn.data, pno=form.pno.data, hours=form.hours.data)
#        db.session.add(employeProject)
#        db.session.commit()
#        flash('You have assigned an employee to a project successfuly !!!')
#        return redirect(url_for('assign'))
#    return render_template('assign.html', title='Assign Employee to Project', form=form, legend='New Project Assignment')

# *** route to remove employee from project
#@app.route("/remove", methods=['GET', 'POST'])
#@login_required
#def remove():
#    form = RemoveFromProject()
#    if form.validate_on_submit():
#        remEmployee = Works_On.query.filter_by(essn=form.essn.data, pno=form.pno.data).first()
#        db.session.delete(remEmployee)
#        db.session.commit()
#        return redirect(url_for('remove'))
#        flash('Employee has been successfuly removed from project !!!')
#    return render_template('remove.html', title='Remove Employee from Project', form=form, legend='Remove Project Assignment')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

# TODO add book route to show books and users 
# TODO add book update and delete 
# TODO add users update and delete 

# *** route to assign employee to project
#@app.route("/add_blood_supplied", methods=['GET', 'POST'])
#@login_required
#def add_blood_supplied():
#    form = AddBloodSupplied()
#    if form.validate_on_submit():
#        addSupply = Blood_Supplied(Donation_ID=form.Donation_ID.data, Health_Facility_Name=form.Health_Facility_Name.data, Blood_Group=form.Blood_Group.data,
#                    Quantity_Supplied=form.Quantity_Supplied.data, Date_of_Supply=form.Date_of_Supply.data)
#        db.session.add(addSupply)
#        db.session.commit()
#        flash('You have successfuly added blood supplied record !!!')
#        return redirect(url_for('add_blood_supplied'))
#    return render_template('add_blood_supplied.html', title='Add Blood Supplied', form=form, legend='New Blood Supplied')







##
