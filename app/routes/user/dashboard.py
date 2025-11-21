from app import app
from flask import render_template, session, flash, redirect, url_for
from app.models.user import User

@app.route('/dashboard')
def dashboard():
     user_id = session.get('user_id')


     if user_id:
          user = User.get_by_id(user_id)
          if user:
              return render_template('user/index.html', user=user)
          else:
              flash('User not found', 'danger')
              return redirect(url_for('login'))
     else:
          flash('You need to log in first to access your dashboard', 'danger')
          return redirect(url_for('login'))
     
