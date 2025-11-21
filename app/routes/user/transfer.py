from app import app
from flask import render_template, session, request, redirect, url_for, flash
from app.models.user import User, Transaction
from .reciept import generate_receipt
import re


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
     user_id = session.get('user_id')
     if user_id:
          user = User.get_by_id(user_id)
          if not user:
              flash('User not found', 'danger')
              return redirect(url_for('login'))


          if request.method == 'POST':
               try:
                    recipient_card_name = request.form['card_name'].strip()
                    recipient_card_number = request.form['card_number']
                    amount = float(request.form['amount'])

                    cleaned_card_number = re.sub(r'\D', '', recipient_card_number)
                    
                    if len(cleaned_card_number) != 16:
                         flash('Card number must be exactly 16 digits.', 'danger')
                         return redirect(url_for('transfer'))

                    cleaned_user_card_number = re.sub(r'\D', '', str(user['card_number']))
                    
                    if cleaned_card_number == cleaned_user_card_number:
                         flash('Cannot send funds to yourself. Please enter a different recipient card number.', 'danger')
                         return redirect(url_for('transfer'))

                    if amount <= 0:
                         flash('Amount must be greater than zero', 'danger')
                         return redirect(url_for('transfer'))

                    if amount > user['balance']:
                         flash('Insufficient Funds', 'danger')
                         return redirect(url_for('transfer'))
                    
                    # Query recipient using cleaned card number
                    recipient = User.get_by_card_number(cleaned_card_number)

                    if not recipient:
                         flash('Invalid recipient card number. Please verify the card number and try again.', 'danger')
                         return redirect(url_for('transfer'))

                    # Check if recipient name matches
                    if recipient['full_name'].upper() != recipient_card_name.upper():
                         flash('Recipient card name does not match the card number.', 'danger')
                         return redirect(url_for('transfer'))

                    # Check if the recipient is not the same as the sender
                    if recipient['id'] == user_id:
                         flash('Cannot send funds to yourself.', 'danger')
                         return redirect(url_for('transfer'))
                    
                    # Update sender's balance
                    User.subtract_from_balance(user_id, amount)

                    # Update recipient's balance
                    User.add_to_balance(recipient['id'], amount)

                    # Create transaction records
                    Transaction.create(
                         user_id=user_id,
                         recipient_name=recipient['full_name'],
                         recipient_card_number=recipient['card_number'],
                         amount=amount,
                         transaction_type='Debit'
                    )

                    Transaction.create(
                         user_id=recipient['id'],
                         recipient_name=user['full_name'],
                         recipient_card_number=user['card_number'],
                         amount=amount,
                         transaction_type='Credit'
                    )

                    # Generate receipt (optional - won't fail if PDF generation unavailable)
                    try:
                         reciept_data = {
                              'sender_name': user['full_name'],
                              'recipient_name': recipient['full_name'],
                              'recipient_card_number': recipient['card_number'],
                              'amount': amount
                         }

                         receipt_filename = generate_receipt(reciept_data)
                         
                         if receipt_filename:
                              return redirect(url_for('payment', filename=receipt_filename))
                         else:
                              flash(f'Successfully transferred ₦{amount:.2f} to {recipient["full_name"]}.', 'success')
                              return redirect(url_for('dashboard'))
                    except Exception as e:
                         flash(f'Successfully transferred ₦{amount:.2f} to {recipient["full_name"]}.', 'success')
                         return redirect(url_for('dashboard'))
               
               except ValueError:
                    flash('Invalid amount entered', 'danger')
                    return redirect(url_for('transfer'))
               except Exception as e:
                    flash(f'Transfer failed: {str(e)}', 'danger')
                    return redirect(url_for('transfer'))



          return render_template('user/transfer.html', user=user)
     else:
          flash('You need to be log in first', 'danger')
          return redirect(url_for('login'))


