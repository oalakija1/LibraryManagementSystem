from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Books, Inventory, Borrower_Copies, Borrower
from wtforms.fields.html5 import DateField



#***********************************************************************************************************
#QUERIES BELOW ARE FOR DROP DOWN MENU PURPOSE
# Query the database to list names of helath care facilities
#healthFacilityNames = Hospital_List.query.with_entities(Hospital_List.Hospital_Name).distinct().order_by(Hospital_List.Hospital_Name)
#result1=list()
#for row in healthFacilityNames:
#    rowDict=row._asdict()
#    result1.append(rowDict)
#myChoice1 = [(row['Hospital_Name'],row['Hospital_Name']) for row in result1]

#***********************************************************************************************************

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



# *** Form to Assign emplyee to a project - Works_on table
#class AddBloodSupplied(FlaskForm):
#    Donation_ID = TextAreaField("Donation ID", validators=[DataRequired()])
#    Health_Facility_Name = SelectField("Health Care Facility", validators=[DataRequired()], choices=myChoice1)  # myChoice1 defined at top
#    Blood_Group = SelectField("Blood Group", validators=[DataRequired()], choices=myChoice2)  # myChoice2 defined at top
#    Quantity_Supplied = IntegerField("Quantity Supplied", validators=[DataRequired()])
#    Date_of_Supply = DateField ("Date of Supply", format='%Y-%m-%d', validators=[DataRequired()])
#    submit = SubmitField('Add Blood Supplied')




#class DeptUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#    dnumber = HiddenField("")
#    dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])
#    mgr_ssn = SelectField("Manager's SSN", choices=myChoices)  # myChoices defined at top
#    mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
#    submit = SubmitField('Update this department')


#    def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
#         dept = Department.query.filter_by(dname=dname.data).first()
#         if dept and (str(dept.dnumber) != str(self.dnumber.data)):
#             raise ValidationError('That department name is already being used. Please choose a different name.')
