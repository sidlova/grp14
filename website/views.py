from flask import Blueprint, abort, jsonify, render_template, request, redirect, session, url_for, flash
from flask_login import login_required, current_user
from .models import SavedFinancialAid, User, FinancialAid
from . import db
from datetime import date, datetime


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

# View financial aids
@views.route('/finacial-aid', methods=['GET'])
def get_financial_aid():
    financial_aids = FinancialAid.query.all()
    serialized_financial_aids = [{'id': financial_aid.id, 'title': financial_aid.title,
                                 'type': financial_aid.type,
                                 'description': financial_aid.description,
                                 'opening_date': financial_aid.opening_date.strftime('%Y-%m-%d'),
                                 'deadline': financial_aid.deadline.strftime('%Y-%m-%d'),
                                 'eligibility_criteria': financial_aid.eligibility_criteria,
                                 'contact_details': financial_aid.contact_details,
                                 'link_to_more_information': financial_aid.link_to_more_information,
                                 'type': financial_aid.type} for financial_aid in financial_aids]

    return render_template('financial_aid.html', financial_aid=serialized_financial_aids, user=current_user)

# Edit financial aid
@views.route('/edit_financial_aid/<int:financial_aid_id>', methods=['GET', 'POST'])
def edit_financial_aid(financial_aid_id):
    financial_aid = FinancialAid.query.get(financial_aid_id)
    if not financial_aid:
        return abort(404)

    if request.method == 'GET':
        title = financial_aid.title
        type = financial_aid.type 
        description = financial_aid.description
        opening_date = financial_aid.opening_date  
        deadline = financial_aid.deadline
        eligibility_criteria = financial_aid.eligibility_criteria
        contact_details = financial_aid.contact_details
        link_to_more_information = financial_aid.link_to_more_information

        return render_template('edit_financial_aid.html', title=title, type=type, financial_aid_id=financial_aid_id,
                               description=description, opening_date=opening_date, deadline=deadline,
                               eligibility_criteria=eligibility_criteria, contact_details=contact_details,
                               link_to_more_information=link_to_more_information)

    else:
        title = request.form['title']
        type = request.form['type']
        description = request.form['description']
        opening_date = request.form['opening_date']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d').date()  
        eligibility_criteria = request.form['eligibility_criteria']
        contact_details = request.form['contact_details']
        link_to_more_information = request.form['link_to_more_information']
        type = request.form['type']  

        financial_aid.title = title
        financial_aid.type = type
        financial_aid.description = description
        financial_aid.deadline = deadline
        financial_aid.eligibility_criteria = eligibility_criteria
        financial_aid.contact_details = contact_details
        financial_aid.link_to_more_information = link_to_more_information
        financial_aid.type = type  

        db.session.commit()
        flash('Financial Aid updated successfully!', category='success')
        return redirect(url_for('views.admin'))  
    
@views.route('/delete_financial_aid/<int:financial_aid_id>', methods=['POST'])
def delete_financial_aid(financial_aid_id):
    financial_aid = FinancialAid.query.get(financial_aid_id)
    if not financial_aid:
        return "Financial aid not found", 404

    db.session.delete(financial_aid)
    db.session.commit()

    saved_financial_aids = SavedFinancialAid.query.filter_by(financial_aid_id=financial_aid_id).all()
    for saved_financial_aid in saved_financial_aids:
        db.session.delete(saved_financial_aid)
        db.session.commit()

    return redirect(url_for('views.admin_view_financial_aids'))
    

@views.route('/add_financial_aid', methods=['GET', 'POST'])
@login_required
def add_financial_aid():
    if request.method == 'POST':
        title = request.form.get('title')
        type = request.form.get('type')  
        description = request.form.get('description')
        eligibility_criteria = request.form.get('eligibility_criteria')
        opening_date = request.form.get('opening_date')  
        deadline = request.form.get('deadline') 
        contact_details = request.form.get('contact_details')
        link_to_more_information = request.form.get('link_to_more_information')

        if not title or not description or not eligibility_criteria or not opening_date or not deadline:
            flash('Please fill in all required fields.', category='error')
            return render_template('add_financial_aid.html')

        try:
            opening_date_datetime = datetime.strptime(opening_date, "%Y-%m-%d")
        except ValueError:
            flash('Invalid opening date format. Please use YYYY-MM-DD.', category='error')
            return render_template('add_financial_aid.html')

        try:
            deadline_datetime = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            flash('Invalid deadline format. Please use YYYY-MM-DD.', category='error')
            return render_template('add_financial_aid.html')

        opening_date_str = opening_date
        deadline_str = deadline

        new_financial_aid = FinancialAid(
            title=title,
            type=type,  
            description=description,
            eligibility_criteria=eligibility_criteria,
            opening_date=date.fromisoformat(opening_date_str),
            deadline=date.fromisoformat(deadline_str),
            contact_details=contact_details,
            link_to_more_information=link_to_more_information
        )
        db.session.add(new_financial_aid)
        db.session.commit()

        flash('Financial Aid added successfully!', category='success')
        return redirect(url_for('views.admin'))

    return render_template('add_financial_aid.html')

@views.route('/financial_aids')
def financial_aids():
    if request.method == 'POST' and 'back_to_financial_aids' in request.form:
        return redirect(url_for('financial_aids'))
    
    financial_aids = FinancialAid.query.all()
    scholarships = [aid for aid in financial_aids if aid.type.lower() == "scholarship"]
    bursaries = [aid for aid in financial_aids if aid.type.lower() == "bursary"]
    grants = [aid for aid in financial_aids if aid.type.lower() == "grant"]
    internships = [aid for aid in financial_aids if aid.type.lower() == "internship"]

    return render_template('financial_aids.html', data=financial_aids, scholarships=scholarships, bursaries=bursaries, grants=grants, internships=internships, user=current_user)

@views.route('/financial_aid/scholarship/<int:financial_aid_id>')
def get_scholarship(financial_aid_id):
    scholarship = FinancialAid.query.get_or_404(financial_aid_id)
    return render_template('scholarship.html', aid=scholarship, user=current_user)

@views.route('/financial_aid/bursary/<int:financial_aid_id>')
def get_bursary(financial_aid_id):
    bursary = FinancialAid.query.get_or_404(financial_aid_id)
    return render_template('bursaries.html', aid=bursary, user=current_user)

@views.route('/financial_aid/internship/<int:financial_aid_id>')
def get_internship(financial_aid_id):
    internship = FinancialAid.query.get_or_404(financial_aid_id)
    return render_template('internship.html', aid=internship, user=current_user)

@views.route('/financial_aid/grant/<int:financial_aid_id>')
def get_grant(financial_aid_id):
    grant = FinancialAid.query.get_or_404(financial_aid_id)
    return render_template('scholarship.html', aid=grant, user=current_user)

@views.route('/save_financial_aid/<int:financial_aid_id>', methods=['POST'])
def save_financial_aid(financial_aid_id):
    if not current_user.is_authenticated:
        flash('Please log in to save financial aid.', 'danger')
        return redirect(url_for('login'))

    aid = FinancialAid.query.get_or_404(financial_aid_id)

    if SavedFinancialAid.query.filter_by(user_id=current_user.id, financial_aid_id=financial_aid_id).first():
        flash('You have already saved this financial aid.', category='error')
        return redirect(url_for('views.financial_aids', financial_aid_id=financial_aid_id))

    saved_aid = SavedFinancialAid(user_id=current_user.id, financial_aid_id=financial_aid_id, date_saved=datetime.now())
    db.session.add(saved_aid)
    db.session.commit()
    flash('Financial aid saved successfully.', category='success')
    url_for('views.financial_aids', financial_aid_id=financial_aid_id, user=current_user)


@views.route('/back_to_financial_aids')
def back_to_financial_aids():
    return redirect(url_for('financial_aids'))


@views.route('/saved_financial_aids', methods=['GET'])
@login_required
def saved_financial_aids():
  search_term = request.args.get('search_term')  # Get search term from form data
  saved_financial_aid_ids = SavedFinancialAid.query.filter(SavedFinancialAid.user_id == current_user.id).with_entities(SavedFinancialAid.financial_aid_id)

  if search_term:
    saved_financial_aid_ids = saved_financial_aid_ids.filter(FinancialAid.title.like(f'%{search_term}%'))

  saved_financial_aid = FinancialAid.query.filter(FinancialAid.id.in_(saved_financial_aid_ids)).all()
  return render_template('saved_financial_aid.html', saved_financial_aid=saved_financial_aid, user=current_user)

# @views.route('/remove_financial_aid', methods=['POST'])
# def remove_financial_aid():
#     financial_aid_id = request.form['financial_aid_id']
#     financial_aid = FinancialAid.query.get(financial_aid_id)
#     if financial_aid:
#         db.session.delete(financial_aid)
#         db.session.commit()
#     return redirect(url_for('home'))


@views.route('/admin')
def admin():
    admin_email = 'BursaryboostAdmin@gmail.com'
    admin_password = 'BursaryboostAdmin'
    if request.method == 'POST':
        if request.form['email'] == admin_email and request.form['password'] == admin_password:
            return redirect(url_for('admin_view'))
        else:
            flash('Invalid email or password')
    users = User.query.all()

    return render_template('admin_dashboard.html',users=users, user=current_user)

@views.route('/admin_view_financial_aids')
def admin_view():
    if 'email' not in session or session['email'] != 'BursaryboostAdmin@gmail.com':
        return redirect(url_for('auth.login'))

    financial_aids = FinancialAid.query.all()
    return render_template('admin_view_financial_aids.html', financial_aids=financial_aids, user=current_user)

@views.route('/admin_view_users')
def admin_view_users():
    if 'email' not in session or session['email'] != 'BursaryboostAdmin@gmail.com':
        return redirect(url_for('auth.login'))
    users = User.query.all()
    return render_template('admin_view_users.html', users=users, user=current_user)


@views.route('/admin/financial_aids', methods=['GET'])
def admin_view_financial_aids():
    financial_aids = FinancialAid.query.all()
    return render_template('admin_view_financial_aids.html', financial_aids=financial_aids, user=current_user)


@views.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if 'email' not in session or session['email'] != 'BursaryboostAdmin@gmail.com':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.gender = request.form['gender']
        user.age = request.form['age']

        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('views.admin_view_users'))

    return render_template('edit_user.html', user=user)

@views.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if 'email' not in session or session['email'] != 'BursaryboostAdmin@gmail.com':
        return redirect(url_for('auth.login'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', category='success')
    return redirect(url_for('views.admin_view_users') ,user=user)

@views.route('/financial_aid/search', methods=['GET'])
def search_financial_aid():
    search_query = request.args.get('search_query')
    financial_aid_list = FinancialAid.query.filter((FinancialAid.title.like('%' + search_query + '%')) | (FinancialAid.description.like('%' + search_query + '%'))).all()
    return render_template('financial_aid_search.html', financial_aid_list=financial_aid_list, search_query=search_query)

@views.route('/about')
def about():
    return render_template('about.html')


# @views.route('/view_details/<financial_aid_id>/<financial_aid_type>')
# def view_details(financial_aid_id, financial_aid_type):
#     if financial_aid_type == 'scholarship':
#         financial_aid = Scholarship.query.get_or_404(financial_aid_id)
#         return render_template('get_scholarship.html',financial_aid=financial_aid)
#     elif financial_aid_type == 'bursary':
#         financial_aid = Bursary.query.get_or_404(financial_aid_id)
#         return render_template('get_bursary.html', financial_aid=financial_aid)
#     elif financial_aid_type == 'grant':
#         financial_aid = Grant.query.get_or_404(financial_aid_id)
#         return render_template('get_grant.html', financial_aid=financial_aid)
#     elif financial_aid_type == 'internship':
#         financial_aid = Internship.query.get_or_404(financial_aid_id)
#         return render_template('get_internship.html', financial_aid=financial_aid)
#     else:
#         return abort(404)