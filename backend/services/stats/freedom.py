from datetime import datetime

from sqlalchemy import case, extract, func

import models
from services.stats.common import USER_ID_MOCK


def get_freedom_projection(db, year: int, account_id: int | None = None):
    total_query = db.query(
        func.sum(
            case((models.Transaction.type == models.TransactionType.income, models.Transaction.amount), else_=0)
        )
        - func.sum(
            case((models.Transaction.type == models.TransactionType.expense, models.Transaction.amount), else_=0)
        )
        - func.sum(
            case((models.Transaction.type == models.TransactionType.invest, models.Transaction.amount), else_=0)
        )
    ).filter(
        models.Transaction.user_id == USER_ID_MOCK,
        models.Transaction.is_paid == True,
    )

    if account_id:
        total_query = total_query.filter(models.Transaction.account_id == account_id)

    total_res = total_query.scalar() or 0

    monthly_query = db.query(
        extract("month", models.Transaction.date).label("month"),
        func.sum(
            case((models.Transaction.type == models.TransactionType.income, models.Transaction.amount), else_=0)
        )
        - func.sum(
            case((models.Transaction.type == models.TransactionType.expense, models.Transaction.amount), else_=0)
        )
        - func.sum(
            case((models.Transaction.type == models.TransactionType.invest, models.Transaction.amount), else_=0)
        ),
    ).filter(
        models.Transaction.user_id == USER_ID_MOCK,
        models.Transaction.is_paid == True,
        extract("year", models.Transaction.date) == year,
    )

    if account_id:
        monthly_query = monthly_query.filter(models.Transaction.account_id == account_id)

    monthly_data = monthly_query.group_by("month").all()

    net_savings_list = [float(row[1]) for row in monthly_data if row[1] is not None]
    avg_monthly_savings = sum(net_savings_list) / len(net_savings_list) if net_savings_list else 0

    current_month = datetime.now().month
    this_year = datetime.now().year
    months_left = (12 - current_month) if year == this_year else (0 if year < this_year else 12)
    projected_december = float(total_res) + (avg_monthly_savings * months_left)

    return {
        "current_balance": float(total_res),
        "avg_monthly_savings": round(avg_monthly_savings, 2),
        "projected_december": round(projected_december, 2),
        "months_left": months_left,
        "data_points": len(net_savings_list),
    }