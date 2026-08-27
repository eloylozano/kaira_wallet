from sqlalchemy import extract

import models

USER_ID_MOCK = 1


def paid_user_transactions(db, account_id: int | None = None):
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == USER_ID_MOCK,
        models.Transaction.is_paid == True,
    )
    if account_id:
        query = query.filter(models.Transaction.account_id == account_id)
    return query


def user_transactions(db, account_id: int | None = None):
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == USER_ID_MOCK,
    )
    if account_id:
        query = query.filter(models.Transaction.account_id == account_id)
    return query


def filter_by_year(query, year: int):
    return query.filter(extract("year", models.Transaction.date) == year)


def filter_by_month(query, month: int):
    return query.filter(extract("month", models.Transaction.date) == month)


def amount(value) -> float:
    return float(value or 0)