from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from sqlalchemy import func, cast, Date, extract

router = APIRouter(prefix="/stats", tags=["Stats"])
USER_ID_MOCK = 1  # ID temporal para saltar la seguridad

@router.get("/", response_model=schemas.TransactionStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Obtiene estadísticas generales de transacciones"""
    try:
        transactions = db.query(models.Transaction).filter(
            models.Transaction.user_id == USER_ID_MOCK
        ).all()
        
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
            "variable_transactions": variable_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

@router.get("/by-category/")
def get_stats_by_category(
    transaction_type: schemas.TransactionType,
    db: Session = Depends(get_db)
):
    """Obtiene gastos/ingresos agrupados por nombre de categoría"""
    try:
        transactions = db.query(models.Transaction).filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.type == transaction_type
        ).all()
        
        stats = {}
        for transaction in transactions:
            # Accedemos al nombre a través de la relación definida en models.py
            category_name = transaction.category.name
            stats[category_name] = stats.get(category_name, 0) + transaction.amount
        
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas por categoría: {str(e)}"
        )
        

@router.get("/daily-expenses")
def get_daily_expenses(db: Session = Depends(get_db)):
    try:
        results = (
            db.query(
                cast(models.Transaction.date, Date).label("day"),
                func.sum(models.Transaction.amount).label("total")
            )
            .filter(
                models.Transaction.user_id == USER_ID_MOCK,
                models.Transaction.type == models.TransactionType.expense
            )
            .group_by("day")
            .order_by("day")
            .all()
        )

        return {str(r.day): float(r.total) for r in results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/monthly")
def get_monthly_stats(year: int, month: int, db: Session = Depends(get_db)):
    """Obtiene el resumen de ingresos y gastos de un mes específico"""
    try:
        sql_month = month + 1
        # Filtramos directamente en la base de datos por año y mes
        query = db.query(models.Transaction).filter(
            models.Transaction.user_id == USER_ID_MOCK,
            extract('year', models.Transaction.date) == year,
            extract('month', models.Transaction.date) == sql_month
        )

        transactions = query.all()

        income = sum(t.amount for t in transactions if t.type == models.TransactionType.income)
        expense = sum(t.amount for t in transactions if t.type == models.TransactionType.expense)
        
        savings_amount = income - expense
        savings_percent = (savings_amount / income * 100) if income > 0 else 0

        return {
            "income": float(income),
            "expense": float(expense),
            "savings_amount": float(savings_amount),
            "savings_percent": round(savings_percent, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/monthly-breakdown")
def get_monthly_breakdown(year: int, db: Session = Depends(get_db)):
    """
    Devuelve ingresos, gastos e inversiones agrupados por mes (solo pagados)
    """

    try:
        rows = (
            db.query(
                extract('month', models.Transaction.date).label("month"),
                models.Transaction.type,
                func.sum(models.Transaction.amount).label("total")
            )
            .filter(
                models.Transaction.user_id == USER_ID_MOCK,
                extract('year', models.Transaction.date) == year,
                models.Transaction.is_paid == True   # ✅ AQUÍ EL FIX REAL
            )
            .group_by("month", models.Transaction.type)
            .all()
        )

        data = {
            m: {
                "month": f"{year}-{str(m).zfill(2)}",
                "income": 0,
                "expense": 0,
                "invest": 0
            }
            for m in range(1, 13)
        }

        for r in rows:
            month = int(r.month)

            if r.type == models.TransactionType.income:
                data[month]["income"] += float(r.total or 0)

            elif r.type == models.TransactionType.expense:
                data[month]["expense"] += float(r.total or 0)

            elif r.type == models.TransactionType.invest:
                data[month]["invest"] += float(r.total or 0)

        return list(data.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# main.py

@router.get("/expense-structure")
def get_expense_structure(month: int, year: int, db: Session = Depends(get_db)):
    # Filtramos SOLO pagadas para que la suma sea coherente
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == USER_ID_MOCK,
        models.Transaction.type == models.TransactionType.expense,
        models.Transaction.is_paid == True, # <--- IMPORTANTE
        extract('month', models.Transaction.date) == month,
        extract('year', models.Transaction.date) == year
    ).all()

    fixed_total = sum(t.amount for t in transactions if t.frequency == models.FrequencyType.fixed)
    variable_total = sum(t.amount for t in transactions if t.frequency == models.FrequencyType.variable)
    
    # El total DEBE ser la suma de estos dos
    total = fixed_total + variable_total 

    return {
        "fixed_total": float(fixed_total),
        "variable_total": float(variable_total),
        "total_expense": float(total), # Enviamos el total coherente
        "fixed_ratio": (fixed_total / total * 100) if total > 0 else 0
    }
    
@router.get("/monthly-boxes")
def get_monthly_boxes(year: int, month: int, db: Session = Depends(get_db)):

    try:
        sql_month = month  # ya viene 1-12 desde frontend

        # Traemos todo el mes en una sola query
        transactions = db.query(models.Transaction).filter(
            models.Transaction.user_id == USER_ID_MOCK,
            extract("year", models.Transaction.date) == year,
            extract("month", models.Transaction.date) == sql_month,
            models.Transaction.is_paid == True  # 🔥 IMPORTANTE
        ).all()

        income = 0
        expense = 0
        invest = 0

        for t in transactions:
            amount = float(t.amount)

            if t.type == models.TransactionType.income:
                income += amount
            elif t.type == models.TransactionType.expense:
                expense += amount
            elif t.type == models.TransactionType.invest:
                invest += amount

        savings = income - expense - invest
        net = income - expense

        return {
            "income": income,
            "expense": expense,
            "invest": invest,
            "savings": savings,
            "net": net
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))