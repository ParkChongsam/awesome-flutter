"""
Accounting Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Account, JournalEntry, Transaction

accounting_bp = Blueprint('accounting', __name__, template_folder='../../templates/accounting')


@accounting_bp.route('/')
@login_required
def index():
    """Accounting dashboard"""
    return render_template('index.html')


@accounting_bp.route('/accounts')
@login_required
def accounts():
    """Chart of accounts"""
    accounts = Account.query.filter_by(is_active=True).order_by(Account.account_code).all()
    return render_template('accounts.html', accounts=accounts)


@accounting_bp.route('/journal-entries')
@login_required
def journal_entries():
    """Journal entries list"""
    page = request.args.get('page', 1, type=int)

    entries = JournalEntry.query.order_by(JournalEntry.entry_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('journal_entries.html', entries=entries)


@accounting_bp.route('/reports/balance-sheet')
@login_required
def balance_sheet():
    """Balance sheet report"""
    return render_template('balance_sheet.html')


@accounting_bp.route('/reports/income-statement')
@login_required
def income_statement():
    """Income statement report"""
    return render_template('income_statement.html')
