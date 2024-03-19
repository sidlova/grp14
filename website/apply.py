# from flask import render_template, redirect, url_for, flash
# from flask_login import current_user
# from flask_mail import Mail, Message
# from . import app, db
# from .models import Apply
# from .forms import ApplyForm
# from flask_wtf import FlaskForm
# from wtforms import StringField, IntegerField, SubmitField, FileField
# from wtforms.validators import DataRequired, Email, Length

# class ApplyForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     first_name = StringField('First Name', validators=[DataRequired()])
#     last_name = StringField('Last Name', validators=[DataRequired()])
#     id_number = StringField('ID Number', validators=[DataRequired(), Length(13, 13)])
#     phone_number = StringField('Phone Number', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     gender = StringField('Gender', validators=[DataRequired()])
#     age = IntegerField('Age', validators=[DataRequired()])
#     status = StringField('Status', validators=[DataRequired()])
#     certified_id_document = FileField('Certified ID Document', validators=[DataRequired()])
#     matric_statement = FileField('Matric Statement', validators=[DataRequired()])
#     cv = FileField('CV', validators=[DataRequired()])
#     other_supporting_documents = FileField('Other Supporting Documents', validators=[DataRequired()])
#     submit = SubmitField('Apply Now')




# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
# app.config['MAIL_PASSWORD'] = 'your_email_password'

# mail = Mail(app)

# @app.route('/apply/<int:financial_aid_id>', methods=['GET', 'POST'])
# def apply(financial_aid_id):
#     form = ApplyForm()
#     if form.validate_on_submit():
#         apply = Apply(
#             user_id=current_user.id,
#             title=form.title.data,
#             first_name=form.first_name.data,
#             last_name=form.last_name.data,
#             id_number=form.id_number.data,
#             phone_number=form.phone_number.data,
#             email=form.email.data,
#             gender=form.gender.data,
#             age=form.age.data,
#             status=form.status.data,
#             certified_id_document=form.certified_id_document.data,
#             matric_statement=form.matric_statement.data,
#             cv=form.cv.data,
#             other_supporting_documents=form.other_supporting_documents.data
#         )
#         db.session.add(apply)
#         db.session.commit()

#         # Send email to user
#         msg = Message('Application Received', sender='your_email@gmail.com', recipients=[form.email.data])
#         msg.body = 'Thank you for applying for the financial aid. Your application has been received and will be reviewed shortly.'
#         mail.send(msg)

#         # Flash success message and redirect to financial aids page
#         flash('Application submitted successfully!', 'success')
#         return redirect(url_for('views.financial_aids'))
#     return render_template('apply.html', form=form)

# from werkzeug.utils import secure_filename

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']

# @app.route('/apply/<int:financial_aid_id>', methods=['GET', 'POST'])
# def apply(financial_aid_id):
#     form = ApplyForm()
#     if form.validate_on_submit():
#         # Handle file uploads
#         certified_id_document = form.certified_id_document.data
#         matric_statement = form.matric_statement.data
#         cv = form.cv.data
#         other_supporting_documents = form.other_supporting_documents.data

#         if certified_id_document and allowed_file(certified_id_document.filename):
  