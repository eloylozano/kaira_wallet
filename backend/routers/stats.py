from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from services import stats as stats_service

router = APIRouter(prefix="/stats", tags=["Stats"])


def run_stats_action(action, error_message: str):
    try:
        return action()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error_message}: {str(exc)}",
        )


@router.get("/", response_model=schemas.TransactionStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_stats(db),
        "Error al obtener estadisticas",
    )


@router.get("/by-category/")
def get_stats_by_category(
    transaction_type: schemas.TransactionType,
    db: Session = Depends(get_db),
):
    return run_stats_action(
        lambda: stats_service.get_stats_by_category(db, transaction_type),
        "Error al obtener estadisticas por categoria",
    )


@router.get("/daily-expenses")
def get_daily_expenses(db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_daily_expenses(db),
        "Error al obtener gastos diarios",
    )


@router.get("/monthly")
def get_monthly_stats(year: int, month: int, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_monthly_stats(db, year, month),
        "Error al obtener estadisticas mensuales",
    )


@router.get("/monthly-breakdown")
def get_monthly_breakdown(year: int, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_monthly_breakdown(db, year),
        "Error al obtener desglose mensual",
    )


@router.get("/expense-structure")
def get_expense_structure(month: int, year: int, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_expense_structure(db, month, year),
        "Error al obtener estructura de gastos",
    )


@router.get("/monthly-boxes")
def get_monthly_boxes(year: int, month: int, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_monthly_boxes(db, year, month),
        "Error al obtener cajas mensuales",
    )


@router.get("/distribution/expenses")
def get_expense_distribution(year: int, month: int, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_expense_distribution(db, year, month),
        "Error al obtener distribucion de gastos",
    )


@router.get("/distribution/pareto")
def get_pareto_data(year: int, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_pareto_data(db, year),
        "Error al obtener datos pareto",
    )


@router.get("/distribution/investments")
def get_investment_distribution(
    year: int,
    month: int | None = None,
    db: Session = Depends(get_db),
):
    return run_stats_action(
        lambda: stats_service.get_investment_distribution(db, year, month),
        "Error al obtener distribucion de inversiones",
    )


@router.get("/summary", response_model=schemas.TransactionStatsResponse)
def get_transaction_summary(year: int | None = None, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_transaction_summary(db, year),
        "Error al calcular estadisticas",
    )


@router.get("/equity/evolution")
def get_equity_evolution(db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_equity_evolution(db),
        "Error al obtener evolucion patrimonial",
    )


@router.get("/equity/asset-types")
def get_asset_type_distribution(db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_asset_type_distribution(db),
        "Error al obtener tipos de activos",
    )


@router.get("/freedom-projection")
def get_freedom_projection(year: int, db: Session = Depends(get_db)):
    return run_stats_action(
        lambda: stats_service.get_freedom_projection(db, year),
        "Error al obtener proyeccion de libertad",
    )
