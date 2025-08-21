from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,StringField, BooleanField, RadioField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length,Regexp, ValidationError
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name is required')])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

def validate_no_special_chars(form, field):
    """Validator to reject special characters (only allow letters, numbers, spaces, and basic punctuation)"""
    if field.data:
        pattern = r'^[a-zA-Z0-9\s\.,\-\\/]+$'
        if not re.match(pattern, field.data):
            raise ValidationError('Special characters are not allowed in this field(Street_address,apartment,city).')

def validate_phone(form, field):
    if not re.match(r'^[0-9]{10}$', field.data):
        raise ValidationError('Please enter a valid 10-digit mobile number (no special characters)')

class PaymentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), validate_no_special_chars])
    company_name = StringField('Company Name', validators=[validate_no_special_chars])
    street_address = StringField('Street Address', validators=[DataRequired(), validate_no_special_chars])
    apartment = StringField('Apartment, Floor, etc (Optional)', validators=[validate_no_special_chars])
    city = StringField('Tower/City', validators=[DataRequired(), validate_no_special_chars])
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        validate_phone 
    ])
    email = StringField('Email Address', validators=[
        DataRequired(), 
        Email(message='Please enter a valid email address (e.g., example@domain.com)')
    ])
    save_info = BooleanField('Save this information for faster check-out next time')
    payment_method = RadioField(
        'Payment Method',
        choices=[('cash', 'Cash on delivery'), ('online', 'Online Payment')],
        default='cash'
    )

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[
    DataRequired(),
    Regexp(
        r'^[0-9]{10}$', 
        message='Phone must be 10 digits (0-9) with no spaces, hyphens, or special characters'
    )
])
    subject = RadioField('Subject', choices=[
        ('General Inquiry', 'General Inquiry'),
        ('Call Request', 'Call Request'),
        ('Complaint', 'Complaint'),
        ('Information', 'Information')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', 
    validators=[
        DataRequired(), 
        Length(min=10, message='Message must be at least 10 characters')
    ],
    render_kw={"placeholder": "write your message.."}
)
    submit = SubmitField('Send Message')