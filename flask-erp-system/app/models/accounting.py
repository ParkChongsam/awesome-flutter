"""
Accounting and Finance Models
"""
from datetime import datetime
from app import db


class Account(db.Model):
    """Chart of accounts"""
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    account_name = db.Column(db.String(200), nullable=False)

    # Account classification
    account_type = db.Column(db.String(50), nullable=False)  # asset, liability, equity, revenue, expense
    account_subtype = db.Column(db.String(50))  # current_asset, fixed_asset, etc.

    # Hierarchy
    parent_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    level = db.Column(db.Integer, default=1)

    # Balance
    opening_balance = db.Column(db.Numeric(15, 2), default=0)
    current_balance = db.Column(db.Numeric(15, 2), default=0)
    debit_balance = db.Column(db.Numeric(15, 2), default=0)
    credit_balance = db.Column(db.Numeric(15, 2), default=0)

    # Flags
    is_active = db.Column(db.Boolean, default=True)
    is_system_account = db.Column(db.Boolean, default=False)

    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    children = db.relationship('Account', backref=db.backref('parent', remote_side=[id]))
    transactions = db.relationship('Transaction', backref='account', lazy='dynamic')

    def __repr__(self):
        return f'<Account {self.account_code}: {self.account_name}>'


class JournalEntry(db.Model):
    """Journal entries for accounting transactions"""
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    entry_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    entry_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Reference
    reference_type = db.Column(db.String(50))  # invoice, payment, adjustment, etc.
    reference_id = db.Column(db.Integer)
    reference_number = db.Column(db.String(50))

    # Details
    description = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)

    # Status
    status = db.Column(db.String(20), default='draft')  # draft, posted, voided
    posted_date = db.Column(db.DateTime)

    # Totals (should be balanced)
    total_debit = db.Column(db.Numeric(15, 2), default=0)
    total_credit = db.Column(db.Numeric(15, 2), default=0)

    # User tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions = db.relationship('Transaction', backref='journal_entry', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def is_balanced(self):
        """Check if debits equal credits"""
        return self.total_debit == self.total_credit

    def __repr__(self):
        return f'<JournalEntry {self.entry_number}>'


class Transaction(db.Model):
    """Individual debit/credit transactions"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    journal_entry_id = db.Column(db.Integer, db.ForeignKey('journal_entries.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

    transaction_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500))

    debit_amount = db.Column(db.Numeric(15, 2), default=0)
    credit_amount = db.Column(db.Numeric(15, 2), default=0)

    # Reference
    reference_type = db.Column(db.String(50))
    reference_id = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction JE:{self.journal_entry_id} Account:{self.account_id}>'
