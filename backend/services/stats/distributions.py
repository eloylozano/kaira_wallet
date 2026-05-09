from sqlalchemy import Numeric, extract, func
from sqlalchemy.orm import aliased

import models
from services.stats.common import USER_ID_MOCK, amount


def get_expense_distribution(db, year: int, month: int):
    parent_category = aliased(models.Category)

    results = (
        db.query(
            parent_category.name.label("parent_name"),
            models.Category.name.label("sub_name"),
            func.sum(models.Transaction.amount).label("value"),
        )
        .join(models.Transaction, models.Category.id == models.Transaction.category_id)
        .outerjoin(parent_category, models.Category.parent_id == parent_category.id)
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.type == models.TransactionType.expense,
            models.Transaction.is_paid == True,
            extract("year", models.Transaction.date) == year,
            extract("month", models.Transaction.date) == month,
        )
        .group_by(parent_category.name, models.Category.name)
        .all()
    )

    data = {}
    for row in results:
        parent_name = row.parent_name if row.parent_name else "Otros"
        if parent_name not in data:
            data[parent_name] = {"name": parent_name, "value": 0, "children": []}

        value = amount(row.value)
        data[parent_name]["value"] += value
        data[parent_name]["children"].append({"name": row.sub_name, "value": value})

    return list(data.values())


def get_pareto_data(db, year: int):
    parent_category = aliased(models.Category, name="parent_cat")
    base_category = models.Category

    results = (
        db.query(
            func.coalesce(parent_category.name, base_category.name).label("group_name"),
            func.round(func.cast(func.sum(models.Transaction.amount), Numeric), 2).label("amount"),
        )
        .join(base_category, base_category.id == models.Transaction.category_id)
        .outerjoin(parent_category, base_category.parent_id == parent_category.id)
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.type == models.TransactionType.expense,
            models.Transaction.is_paid == True,
            extract("year", models.Transaction.date) == year,
        )
        .group_by(func.coalesce(parent_category.name, base_category.name))
        .order_by(func.sum(models.Transaction.amount).desc())
        .all()
    )

    total_year = sum(amount(row.amount) for row in results)
    cumulative = 0
    pareto_data = []

    for row in results:
        row_amount = amount(row.amount)
        cumulative += row_amount
        pareto_data.append(
            {
                "name": row.group_name,
                "amount": row_amount,
                "percent": round((cumulative / total_year * 100), 2) if total_year > 0 else 0,
            }
        )

    return pareto_data


def get_investment_distribution(db, year: int, month: int | None = None):
    parent_category = aliased(models.Category, name="parent_cat")

    balance_rows = (
        db.query(
            models.Transaction.type,
            func.sum(models.Transaction.amount).label("total"),
        )
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.is_paid == True,
        )
        .group_by(models.Transaction.type)
        .all()
    )

    totals = {row.type: amount(row.total) for row in balance_rows}
    cash = (
        totals.get(models.TransactionType.income, 0)
        - totals.get(models.TransactionType.expense, 0)
        - totals.get(models.TransactionType.invest, 0)
    )

    query = (
        db.query(
            parent_category.name.label("parent_name"),
            models.Category.name.label("sub_name"),
            models.Transaction.description.label("description"),
            func.sum(models.Transaction.amount).label("value"),
        )
        .join(models.Transaction, models.Category.id == models.Transaction.category_id)
        .outerjoin(parent_category, models.Category.parent_id == parent_category.id)
        .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.type == models.TransactionType.invest,
            models.Transaction.is_paid == True,
            extract("year", models.Transaction.date) == year,
        )
    )

    if month:
        query = query.filter(extract("month", models.Transaction.date) == month)

    results = query.group_by(
        parent_category.name,
        models.Category.name,
        models.Transaction.description,
    ).all()

    data_map = {}
    total_invested = 0

    for row in results:
        parent_name = row.parent_name or "Otros"
        sub_name = row.sub_name or "Sin Categoria"
        description = row.description or "Sin descripcion"
        value = amount(row.value)
        total_invested += value

        if parent_name not in data_map:
            data_map[parent_name] = {"name": parent_name, "children": {}, "value": 0}

        data_map[parent_name]["value"] += value

        if sub_name not in data_map[parent_name]["children"]:
            data_map[parent_name]["children"][sub_name] = {
                "name": sub_name,
                "children": [],
                "value": 0,
            }

        data_map[parent_name]["children"][sub_name]["value"] += value
        data_map[parent_name]["children"][sub_name]["children"].append(
            {
                "name": description,
                "value": value,
            }
        )

    allocation = []
    for node in data_map.values():
        node["children"] = list(node["children"].values())
        allocation.append(node)

    return {
        "cash_ratio": {
            "invested": round(total_invested, 2),
            "cash": round(max(0, cash), 2),
        },
        "allocation": allocation,
    }

