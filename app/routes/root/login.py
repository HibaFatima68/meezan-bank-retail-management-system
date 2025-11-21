from app import app, bcrypt
from flask import render_template, request, redirect, url_for, flash, session
from app.models.user import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = User.get_by_email(email)

            if user and bcrypt.check_password_hash(user['password'], password):
                try:
                    User.ensure_account_and_card(user['id'])
                    user = User.get_by_id(user['id'])
                except Exception as e:
                    print(f"Warning: Could not ensure account/card for user {user['id']}: {str(e)}")
                
                session['user_id'] = user['id']
                flash('Login succesful', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
                return redirect(url_for('login'))
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
            return redirect(url_for('login'))
        
    return render_template('root/login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'session')
    return redirect(url_for('home_page'))
