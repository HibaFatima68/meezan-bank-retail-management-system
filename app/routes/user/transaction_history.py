from app import app
from flask import render_template, session, redirect, flash, url_for
from app.models.user import User
from app.db_utils import TransactionDAO


@app.route('/transaction_history')
def transaction_history():
    user_id = session.get('user_id')

    if not user_id:
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))

    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

    transactions = TransactionDAO.get_by_user_id(user_id)

    # ⭐ ADD THIS DEBUG LINE HERE ⭐
    print("DEBUG TRANSACTIONS RAW:", transactions)

    # Convert Oracle DATE objects to string format
    for t in transactions:
        if t.get("timestamp"):
            try:
                t["timestamp"] = t["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass

    return render_template(
        "user/transaction_history.html",
        user=user,
        transactions=transactions
    )
