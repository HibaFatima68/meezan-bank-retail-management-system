from app import app
from flask import render_template, session, redirect, flash, url_for
from app.models.user import User

@app.route('/locker')
def locker():
     user_id = session.get('user_id')

     if user_id:
          user = User.get_by_id(user_id)
          if not user:
              flash('User not found', 'danger')
              return redirect(url_for('login'))
          return render_template('user/soon.html', user=user)
     else:
          flash('You need to be logged in first', 'danger')
          return redirect(url_for('login'))


