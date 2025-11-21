from app import app
from flask import render_template, session, redirect, flash, url_for
from app.models.user import User, Transaction
from datetime import timedelta, timezone


def convert_to_pakistan_time(utc_datetime):
    if utc_datetime is None:
        return None
    
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
    
    pkt_time = utc_datetime.astimezone(timezone(timedelta(hours=5)))
    
    return pkt_time


@app.route('/transaction_history')
def transaction_history():
    user_id = session.get('user_id')
        
    if user_id:
        user = User.get_by_id(user_id)
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('login'))

        transactions = Transaction.get_by_user_id(user_id, order_by="timestamp DESC")
        
        # Convert timestamps to Pakistan Standard Time
        transactions_with_pkt = []
        for transaction in transactions:
            # Parse timestamp string to datetime if needed
            timestamp = transaction['timestamp']
            if isinstance(timestamp, str):
                from datetime import datetime
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            pkt_timestamp = convert_to_pakistan_time(timestamp)
            transactions_with_pkt.append({
                'transaction': transaction,
                'pkt_timestamp': pkt_timestamp
            })

        return render_template('user/transaction_history.html', user=user, transactions_with_pkt=transactions_with_pkt)
    else:
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
   
