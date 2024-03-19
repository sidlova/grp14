from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for
from .models import User
from flask_login import current_user, login_required
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


profile = Blueprint('profile', __name__)


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        phone_number = request.form.get('phoneNumber')
        email = request.form.get('email')
        gender = request.form.get('gender')
        age = request.form.get('age')

        if len(first_name) < 3:
            flash('First name must be greater than 2 characters.', category='error')
        elif len(last_name) < 3:
            flash('Last name must be greater than 2 characters.', category='error')
        else:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.email = email
            user.gender = gender
            user.age = age

            db.session.commit()
            flash('Profile updated successfully!', category='success')
            return render_template("profile.html", user=current_user)

    return render_template("profile.html", user=current_user)


@profile.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = User.query.get(current_user.id)

    if request.method == 'POST':
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')

        if not check_password_hash(user.password, current_password):
            flash('Incorrect current password.', category='error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', category='error')
        elif len(new_password) < 8:
            flash('New password must be at least 8 characters.', category='error')
        else:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            flash('Password changed successfully!', category='success')
            return redirect(url_for('profile.edit_profile'))

    return render_template("change_password.html", user=user)
