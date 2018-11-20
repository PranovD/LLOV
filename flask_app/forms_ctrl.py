""" This module does blah blah blah """

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import Form, StringField, BooleanField, SubmitField
from wtforms import RadioField, IntegerField, TextField
from wtforms.validators import DataRequired
from flask_app import errors, db
from flask_app import APP



class DogIntakeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    breed = StringField('Breed')
    gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    age = IntegerField("Age")
    weight = IntegerField("Weight")
    comments = TextField("Additional Comments")
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
    email = TextField("Email")

    aggressive = RadioField('Aggressive?',
                            choices=[('Y', 'Yes'), ('N', 'No'),
                                     ('U', 'Unknown')])
    disease = RadioField('Any known diseases?',
                         choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Unknown')])


class VolunteerIntakeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField("Age")
    email = TextField("Email")
    comments = TextField("Additional Comments")


class FosterVolunteerIntakeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField("Age")
    email = TextField("Email")
    comments = TextField("Additional Comments")


class DonationForm(FlaskForm):
    """
    description
    """
    name = StringField('Name', validators=[DataRequired()])
    amount = IntegerField("Amount")


WHITE_LISTED_FORMS = {"Dogs": [DogIntakeForm, "dog_intake_form.html"],
                      "Person": [VolunteerIntakeForm,
                                 "volunteer_intake_form.html"],
                      "donations": [DonationForm, "donation_form.html"]
                      }


def create_form_object(form):
    """
    description
    """
    if form not in WHITE_LISTED_FORMS:
        raise errors.InvalidUsage("We are currently not storing \
                                  this data.", status_code=410)
    return WHITE_LISTED_FORMS[form][0]()


def get_html_form_type(form):
    """
    description
    """
    if form not in WHITE_LISTED_FORMS:
        raise errors.InvalidUsage("We are currently not storing \
                                  this data.", status_code=410)
    return WHITE_LISTED_FORMS[form][1]


