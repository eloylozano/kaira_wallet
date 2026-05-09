from datetime import datetime

from sqlalchemy import case, extract, func

import models
from services.stats.common import USER_ID_MOCK


def get_freedom_projection(db, year: int):
    total_res = (
        db.query(
            func.sum(
                case((models.Transaction.type == models.TransactionType.income, models.Transaction.amount), else_=0)
            )
            - func.sum(
                case((models.Transaction.type == models.TransactionType.expense, models.Transaction.amount), else_=0)
            )
            - func.sum(
                case((models.Transaction.type == models.TransactionType.invest, models.Transaction.amount), else_=0)
            )
        )
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.is_paid == True,
        )
        .scalar()
        or 0
    )

    monthly_data = (
        db.query(
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
        )
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.is_paid == True,
            extract("year", models.Transaction.date) == year,
        )
        .group_by("month")
        .all()
    )

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

