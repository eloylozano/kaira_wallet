from sqlalchemy import case, extract, func

import models
from services.stats.common import USER_ID_MOCK, amount


def get_equity_evolution(db):
    rows = (
        db.query(
            extract("year", models.Transaction.date).label("year"),
            extract("month", models.Transaction.date).label("month"),
            func.sum(
                case(
                    (models.Transaction.type == models.TransactionType.income, models.Transaction.amount),
                    (models.Transaction.type == models.TransactionType.expense, -models.Transaction.amount),
                    (models.Transaction.type == models.TransactionType.invest, -models.Transaction.amount),
                    else_=0,
                )
            ).label("cash_change"),
            func.sum(
                case(
                    (models.Transaction.type == models.TransactionType.invest, models.Transaction.amount),
                    else_=0,
                )
            ).label("invest_change"),
        )
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.is_paid == True,
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    history = []
    cum_cash = 0
    cum_invest = 0

    for row in rows:
        cum_cash += amount(row.cash_change)
        cum_invest += amount(row.invest_change)

        history.append(
            {
                "date": f"{int(row.year)}-{str(int(row.month)).zfill(2)}",
                "cash": round(cum_cash, 2),
                "invested": round(cum_invest, 2),
                "total": round(cum_cash + cum_invest, 2),
            }
        )

    return history


def get_asset_type_distribution(db):
    results = (
        db.query(
            models.Category.name.label("cat_name"),
            models.Transaction.description.label("asset_name"),
            func.sum(models.Transaction.amount).label("total"),
        )
        .join(models.Transaction, models.Category.id == models.Transaction.category_id)
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.type == models.TransactionType.invest,
            models.Transaction.is_paid == True,
        )
        .group_by(models.Category.name, models.Transaction.description)
        .all()
    )

    hierarchy = {}
    for row in results:
        category = row.cat_name
        if category not in hierarchy:
            hierarchy[category] = {"name": category, "children": []}

        hierarchy[category]["children"].append(
            {
                "name": row.asset_name or "Sin nombre",
                "value": amount(row.total),
            }
        )

    return list(hierarchy.values())

