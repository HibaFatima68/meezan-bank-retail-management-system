from app import app
from flask import render_template, session, request, redirect, url_for, flash
from app.models.user import User, Transaction
import re

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
     user_id = session.get('user_id')
     if user_id:
          user = User.get_by_id(user_id)
          if not user:
              flash('User not found', 'danger')
              return redirect(url_for('login'))

          if request.method == 'POST':
               try:
                    card_number = request.form['card_number']
                    amount = float(request.form['amount'])

                    cleaned_card_number = re.sub(r'\D', '', card_number)  # Remove all non-digits
                    
                    if cleaned_card_number != user['card_number']:
                         flash('Invalid card number', 'danger')
                         return redirect(url_for('deposit'))
                    
                    if amount <= 0:
                         flash('Amount must be greater than zero', 'danger')
                         return redirect(url_for('deposit'))
                    
                    User.add_to_balance(user_id, amount)

                    Transaction.create(
                         user_id=user_id,
                         recipient_name=user['full_name'],
                         recipient_card_number=user['card_number'],
                         amount=amount,
                         transaction_type="Credit - Deposit"
                    )
                    
                    flash(f'Successfully deposited ₦{amount:.2f} to your account.', 'success')
                    return redirect(url_for('dashboard'))
               except ValueError:
                    flash('Invalid amount entered', 'danger')
                    return redirect(url_for('deposit'))
               except Exception as e:
                    flash(f'Deposit failed: {str(e)}', 'danger')
                    return redirect(url_for('deposit'))
          
          return render_template('user/deposit.html', user=user)
     else:
          flash('You need to be logged in first', 'danger')
          return redirect(url_for('login'))
