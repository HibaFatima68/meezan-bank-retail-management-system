from app import app
from flask import render_template, session, redirect, flash, url_for, request
from app.models.user import User
from app.db_utils import LockerDAO


@app.route('/locker')
def locker():
    user_id = session.get('user_id')

    if not user_id:
        flash('You need to be logged in first', 'danger')
        return redirect(url_for('login'))

    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

    my_lockers = LockerDAO.get_my_lockers(user_id)

    return render_template(
        'user/lockers/dashboard.html',
        user=user,
        my_lockers=my_lockers
    )


@app.route('/locker/rent', methods=['GET', 'POST'])
def rent_locker():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    user = User.get_by_id(user_id)

    if request.method == 'POST':
        try:
            locker_id = int(request.form.get('locker_id'))

            LockerDAO.rent_locker(user_id, locker_id)
            flash('Locker rented successfully!', 'success')
            return redirect(url_for('locker'))

        except Exception as e:
            flash(f'Error renting locker: {str(e)}', 'danger')

    available_lockers = LockerDAO.get_available_lockers()

    return render_template(
        'user/lockers/rent.html',
        user=user,
        available_lockers=available_lockers
    )
