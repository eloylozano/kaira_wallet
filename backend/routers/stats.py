from fastapi import APIRouter, Depends, HTTPException, Request, status
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
def get_stats(request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_transaction_summary(db, year=None, account_id=account.id),
        "Error al obtener estadisticas",
    )
    

@router.get("/by-category/")
def get_stats_by_category(
    transaction_type: schemas.TransactionType,
    request: Request,
    db: Session = Depends(get_db),
):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_stats_by_category(db, transaction_type, account_id=account.id),
        "Error al obtener estadisticas por categoria",
    )


@router.get("/daily-expenses")
def get_daily_expenses(request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_daily_expenses(db, account_id=account.id),
        "Error al obtener gastos diarios",
    )


@router.get("/monthly")
def get_monthly_stats(year: int, month: int, request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_monthly_stats(db, year, month, account_id=account.id),
        "Error al obtener estadisticas mensuales",
    )


@router.get("/monthly-breakdown")
def get_monthly_breakdown(year: int, request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_monthly_breakdown(db, year, account_id=account.id),
        "Error al obtener desglose mensual",
    )


@router.get("/expense-structure")
def get_expense_structure(month: int, year: int, request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_expense_structure(db, month, year, account_id=account.id),
        "Error al obtener estructura de gastos",
    )


@router.get("/monthly-boxes")
def get_monthly_boxes(year: int, month: int, request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_monthly_boxes(db, year, month, account_id=account.id),
        "Error al obtener cajas mensuales",
    )


@router.get("/distribution/expenses")
def get_expense_distribution(year: int, month: int, request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_expense_distribution(db, year, month, account_id=account.id),
        "Error al obtener distribucion de gastos",
    )


@router.get("/distribution/pareto")
def get_pareto_data(year: int, request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_pareto_data(db, year, account_id=account.id),
        "Error al obtener datos pareto",
    )


@router.get("/distribution/investments")
def get_investment_distribution(
    year: int,
    request: Request,
    month: int | None = None,
    db: Session = Depends(get_db),
):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_investment_distribution(db, year, month, account_id=account.id),
        "Error al obtener distribucion de inversiones",
    )

@router.get("/summary", response_model=schemas.TransactionStatsResponse)
def get_transaction_summary(request: Request, year: int | None = None, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_transaction_summary(db, year, account.id),
        "Error al calcular estadisticas",
    )

@router.get("/equity/evolution")
def get_equity_evolution(request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_equity_evolution(db, account_id=account.id),
        "Error al obtener evolucion patrimonial",
    )


@router.get("/equity/asset-types")
def get_asset_type_distribution(request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_asset_type_distribution(db, account_id=account.id),
        "Error al obtener tipos de activos",
    )


@router.get("/freedom-projection")
def get_freedom_projection(year: int, request: Request, db: Session = Depends(get_db)):
    account = request.state.account
    return run_stats_action(
        lambda: stats_service.get_freedom_projection(db, year, account_id=account.id),
        "Error al obtener proyeccion de libertad",
    )