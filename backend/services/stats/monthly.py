from sqlalchemy import Date, cast, extract, func

import models
from services.stats.common import USER_ID_MOCK, amount, paid_user_transactions, user_transactions


def get_daily_expenses(db):
    results = (
        db.query(
            cast(models.Transaction.date, Date).label("day"),
            func.sum(models.Transaction.amount).label("total"),
        )
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.type == models.TransactionType.expense,
        )
        .group_by("day")
        .order_by("day")
        .all()
    )

    return {str(r.day): amount(r.total) for r in results}


def get_monthly_stats(db, year: int, month: int):
    sql_month = month + 1
    transactions = (
        user_transactions(db)
        .filter(
            extract("year", models.Transaction.date) == year,
            extract("month", models.Transaction.date) == sql_month,
        )
        .all()
    )

    income = sum(t.amount for t in transactions if t.type == models.TransactionType.income)
    expense = sum(t.amount for t in transactions if t.type == models.TransactionType.expense)

    savings_amount = income - expense
    savings_percent = (savings_amount / income * 100) if income > 0 else 0

    return {
        "income": float(income),
        "expense": float(expense),
        "savings_amount": float(savings_amount),
        "savings_percent": round(savings_percent, 2),
    }


def get_monthly_breakdown(db, year: int):
    rows = (
        db.query(
            extract("month", models.Transaction.date).label("month"),
            models.Transaction.type,
            func.sum(models.Transaction.amount).label("total"),
        )
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            extract("year", models.Transaction.date) == year,
            models.Transaction.is_paid == True,
        )
        .group_by("month", models.Transaction.type)
        .all()
    )

    data = {
        month: {
            "month": f"{year}-{str(month).zfill(2)}",
            "income": 0,
            "expense": 0,
            "invest": 0,
        }
        for month in range(1, 13)
    }

    for row in rows:
        month = int(row.month)
        total = amount(row.total)

        if row.type == models.TransactionType.income:
            data[month]["income"] += total
        elif row.type == models.TransactionType.expense:
            data[month]["expense"] += total
        elif row.type == models.TransactionType.invest:
            data[month]["invest"] += total

    return list(data.values())


def get_expense_structure(db, month: int, year: int):
    transactions = (
        paid_user_transactions(db)
        .filter(
            models.Transaction.type == models.TransactionType.expense,
            extract("month", models.Transaction.date) == month,
            extract("year", models.Transaction.date) == year,
        )
        .all()
    )

    fixed_total = sum(t.amount for t in transactions if t.frequency == models.FrequencyType.fixed)
    variable_total = sum(t.amount for t in transactions if t.frequency == models.FrequencyType.variable)
    total = fixed_total + variable_total

    return {
        "fixed_total": float(fixed_total),
        "variable_total": float(variable_total),
        "total_expense": float(total),
        "fixed_ratio": (fixed_total / total * 100) if total > 0 else 0,
    }


def get_monthly_boxes(db, year: int, month: int):
    transactions = (
        paid_user_transactions(db)
        .filter(
            extract("year", models.Transaction.date) == year,
            extract("month", models.Transaction.date) == month,
        )
        .all()
    )

    income = 0
    expense = 0
    invest = 0

    for transaction in transactions:
        transaction_amount = float(transaction.amount)

        if transaction.type == models.TransactionType.income:
            income += transaction_amount
        elif transaction.type == models.TransactionType.expense:
            expense += transaction_amount
        elif transaction.type == models.TransactionType.invest:
            invest += transaction_amount

    return {
        "income": income,
        "expense": expense,
        "invest": invest,
        "savings": income - expense - invest,
        "net": income - expense,
    }

