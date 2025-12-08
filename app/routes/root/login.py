from app import app, bcrypt
from flask import render_template, request, redirect, url_for, flash, session
from app.models.user import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Get the full user dictionary from DB
            user = User.get_by_email(email)

            if not user:
                flash("No user found with this email", "danger")
                return redirect(url_for('login'))

            # Oracle column is PASSWORD_HASH, not 'password'
            stored_hash = user.get('password_hash')

            if stored_hash is None:
                flash("Your account password is missing in the database.", "danger")
                return redirect(url_for('login'))

            # bcrypt password check
            if bcrypt.check_password_hash(stored_hash, password):
                session['user_id'] = user['id']
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password!", "danger")
                return redirect(url_for('login'))

        except Exception as e:
            flash(f"Login error: {str(e)}", "danger")
            return redirect(url_for('login'))

    return render_template('root/login.html')
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'session')
    return redirect(url_for('home_page'))
