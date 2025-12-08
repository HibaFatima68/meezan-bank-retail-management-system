from app import app
from flask import render_template, session, redirect, flash, url_for, request
from app.models.user import User
from app.db_utils import LoanDAO, UserDAO


@app.route('/loan')
def loan():
    user_id = session.get('user_id')

    if not user_id:
        flash('You need to be logged in first', 'danger')
        return redirect(url_for('login'))
    
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

    active_loans = LoanDAO.get_active_loans(user_id)
    applications = LoanDAO.get_applications(user_id)

    return render_template(
        'user/loans/dashboard.html',
        user=user,
        active_loans=active_loans,
        applications=applications
    )


@app.route('/loan/apply', methods=['GET', 'POST'])
def apply_loan():
    user_id = session.get('user_id')

    if not user_id:
        flash('You must be logged in first', 'danger')
        return redirect(url_for('login'))

    user = User.get_by_id(user_id)

    if request.method == 'POST':
        try:
            loan_type_id = int(request.form.get('loan_type_id'))
            amount = float(request.form.get('amount'))

            if amount <= 0:
                raise ValueError("Amount must be positive")

            # Fetch user's account branch_id
            account_id = UserDAO.get_account_id_by_user_id(user_id)
            branch_id = 1  # or fetch dynamically if needed

            LoanDAO.create_application(user_id, branch_id, loan_type_id, amount)
            flash('Loan application submitted successfully!', 'success')
            return redirect(url_for('loan'))

        except Exception as e:
            flash(f'Error applying for loan: {str(e)}', 'danger')

    loan_types = LoanDAO.get_types()

    return render_template(
        'user/loans/apply.html',
        user=user,
        loan_types=loan_types
    )


@app.route('/loan/repay/<int:loan_id>', methods=['POST'])
def repay_loan(loan_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    try:
        amount = float(request.form.get('amount'))
        if amount <= 0:
            raise ValueError("Amount must be positive")

        LoanDAO.repay_installment(loan_id, amount)
        flash('Repayment successful!', 'success')

    except Exception as e:
        flash(f'Repayment failed: {str(e)}', 'danger')

    return redirect(url_for('loan'))
