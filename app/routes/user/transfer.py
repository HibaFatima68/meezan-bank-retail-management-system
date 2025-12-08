from app import app
from flask import render_template, session, request, redirect, url_for, flash
from app.models.user import User, Transaction
from .reciept import generate_receipt
import re


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in.', 'danger')
        return redirect(url_for('login'))

    user = User.get_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    # GET request
    if request.method == 'GET':
        return render_template('user/transfer.html', user=user)

    # POST (transfer)
    try:
        recipient_name = request.form['card_name'].strip()
        recipient_card = request.form['card_number']
        amount = float(request.form['amount'])

        # Clean card
        clean_card = re.sub(r'\D', '', recipient_card)

        if len(clean_card) != 16:
            flash('Card number must be exactly 16 digits.', 'danger')
            return redirect(url_for('transfer'))

        # Prevent self-transfer
        user_card_clean = re.sub(r'\D', '', str(user['card_number']))
        if clean_card == user_card_clean:
            flash('You cannot transfer to your own card.', 'danger')
            return redirect(url_for('transfer'))

        if amount <= 0:
            flash("Amount must be greater than zero.", "danger")
            return redirect(url_for('transfer'))

        if amount > user['balance']:
            flash("Insufficient balance.", "danger")
            return redirect(url_for('transfer'))

        # Validate recipient exists (DB handles name check)
        recipient = User.get_by_card_number(clean_card)
        if not recipient:
            flash("Recipient card not found.", "danger")
            return redirect(url_for('transfer'))

        # Update balances
        User.subtract_from_balance(user_id, amount)
        User.add_to_balance(recipient['id'], amount)

        # Create sender transaction (DEBIT)
        Transaction.create(
            user_id,
            recipient_name,
            clean_card,
            amount,
            "Transfer"
        )

        # Create recipient transaction (CREDIT)
        Transaction.create(
            recipient['id'],
            user['full_name'],
            user_card_clean,
            amount,
            "Deposit"
        )

        # Generate receipt
        try:
            data = {
                'sender_name': user['full_name'],
                'recipient_name': recipient['full_name'],
                'recipient_card_number': recipient['card_number'],
                'amount': amount
            }
            filename = generate_receipt(data)
            if filename:
                return redirect(url_for('payment', filename=filename))
        except:
            pass

        flash(f"Successfully transferred PKR {amount:.2f} to {recipient['full_name']}.", "success")
        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f"Transfer failed: {str(e)}", "danger")
        return redirect(url_for('transfer'))
