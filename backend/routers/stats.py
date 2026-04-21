from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

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