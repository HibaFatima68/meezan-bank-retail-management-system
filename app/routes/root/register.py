from app import app, bcrypt
from flask import render_template, request, flash, redirect, url_for, session
import random
from app.models.user import User


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form.get('phone_number', '').strip()
        address = request.form.get('address', '').strip()
        password =  request.form['password']
        confirm_password = request.form['confirm_password']
    

        
        if password != confirm_password:
            flash('passwords do not match', 'danger')
            return redirect(url_for('register_page'))
        if len(password) < 6:
            flash('Password is too short. Please make it more lengthy', 'danger')
            return redirect(url_for('register_page'))
        
        if phone_number and (len(phone_number) != 11 or not phone_number.isdigit()):
            flash('Phone number must be exactly 11 digits', 'danger')
            return redirect(url_for('register_page'))

        
        user = User.get_by_email(email)
        if user:
            flash('You already have an account. Please log in', 'danger')
            return redirect(url_for('login'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16) ])
        formatted_card_number = '_'.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])

        try:
            new_user_id = User.create(
                full_name=full_name,
                email=email,
                password=hashed_password,
                card_number=card_number,
                phone_number=phone_number if phone_number else None,
                address=address if address else None
            )

            session['user_id'] = new_user_id
            session['card_number'] = formatted_card_number

            flash('Registration Sucessful. Welcome to our Banking Application', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
            return redirect(url_for('register_page'))
    

    return render_template('root/register.html')
