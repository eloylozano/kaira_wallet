from sqlalchemy import extract

import models
from services.stats.common import USER_ID_MOCK, paid_user_transactions, user_transactions


def build_transaction_totals(transactions):
    total_income = sum(t.amount for t in transactions if t.type == models.TransactionType.income)
    total_expense = sum(t.amount for t in transactions if t.type == models.TransactionType.expense)
    total_invest = sum(t.amount for t in transactions if t.type == models.TransactionType.invest)

    fixed_count = len([t for t in transactions if t.frequency == models.FrequencyType.fixed])
    variable_count = len([t for t in transactions if t.frequency == models.FrequencyType.variable])

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "total_invest": total_invest,
        "fixed_transactions": fixed_count,
        "variable_transactions": variable_count,
    }


def get_stats(db):
    transactions = user_transactions(db).all()
    return build_transaction_totals(transactions)


def get_stats_by_category(db, transaction_type):
    transactions = (
        user_transactions(db)
        .filter(models.Transaction.type == transaction_type)
        .all()
    )

    stats = {}
    for transaction in transactions:
        category_name = transaction.category.name
        stats[category_name] = stats.get(category_name, 0) + transaction.amount

    return stats


def get_transaction_summary(db, year: int | None = None):
    query = paid_user_transactions(db)

    if year:
        query = query.filter(extract("year", models.Transaction.date) == year)

    return build_transaction_totals(query.all())

