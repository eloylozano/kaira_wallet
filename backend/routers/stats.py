from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, aliased
import models, schemas
from database import get_db
from sqlalchemy import Numeric, func, cast, Date, extract, case
from sqlalchemy.orm import aliased
from sqlalchemy import func, Numeric

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
    
@router.get("/distribution/expenses")
def get_expense_distribution(year: int, month: int, db: Session = Depends(get_db)):
    try:
        # Alias para poder hacer el join de la categoría con su padre
        ParentCategory = aliased(models.Category)
        
        results = (
            db.query(
                ParentCategory.name.label("parent_name"),
                models.Category.name.label("sub_name"),
                func.sum(models.Transaction.amount).label("value")
            )
            .join(models.Transaction, models.Category.id == models.Transaction.category_id)
            # Join con el padre (si no tiene padre, es que ella misma es nivel superior)
            .outerjoin(ParentCategory, models.Category.parent_id == ParentCategory.id)
            .filter(
                models.Transaction.user_id == USER_ID_MOCK,
                models.Transaction.type == models.TransactionType.expense,
                models.Transaction.is_paid == True,
                extract('year', models.Transaction.date) == year,
                extract('month', models.Transaction.date) == month
            )
            .group_by(ParentCategory.name, models.Category.name)
            .all()
        )

        # Estructuramos para el Treemap
        # Si parent_name es None, usamos el sub_name como principal
        data = {}
        for r in results:
            p_name = r.parent_name if r.parent_name else "Otros"
            if p_name not in data:
                data[p_name] = {"name": p_name, "value": 0, "children": []}
            
            data[p_name]["value"] += float(r.value)
            data[p_name]["children"].append({"name": r.sub_name, "value": float(r.value)})

        return list(data.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- GASTOS: Pareto Anual ---
@router.get("/distribution/pareto")
def get_pareto_data(year: int, db: Session = Depends(get_db)):
    try:
        # 1. Definimos el alias para la categoría padre
        ParentCategory = aliased(models.Category, name="parent_cat")
        # 2. Definimos la categoría base explícitamente para evitar ambigüedad
        BaseCategory = models.Category

        results = (
            db.query(
                # Si tiene padre, usamos el nombre del padre. Si no, el de la categoría base.
                func.coalesce(ParentCategory.name, BaseCategory.name).label("group_name"),
                func.round(func.cast(func.sum(models.Transaction.amount), Numeric), 2).label("amount")
            )
            # Unimos Transacciones -> Categoría Base
            .join(BaseCategory, BaseCategory.id == models.Transaction.category_id)
            # Unimos Categoría Base -> Categoría Padre (Alias)
            .outerjoin(ParentCategory, BaseCategory.parent_id == ParentCategory.id)
            .filter(
                models.Transaction.user_id == USER_ID_MOCK,
                models.Transaction.type == models.TransactionType.expense,
                models.Transaction.is_paid == True,
                extract('year', models.Transaction.date) == year
            )
            .group_by(func.coalesce(ParentCategory.name, BaseCategory.name))
            .order_by(func.sum(models.Transaction.amount).desc())
            .all()
        )

        total_year = sum(float(r.amount) for r in results)
        cumulative = 0
        pareto_data = []

        for r in results:
            amount = float(r.amount)
            cumulative += amount
            pareto_data.append({
                "name": r.group_name,
                "amount": amount,
                "percent": round((cumulative / total_year * 100), 2) if total_year > 0 else 0
            })

        return pareto_data
    except Exception as e:
        print(f"Error en Pareto: {e}") # Para debug en consola
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.get("/distribution/investments")
def get_investment_distribution(year: int, month: int = None, db: Session = Depends(get_db)):
    try:
        ParentCategory = aliased(models.Category, name="parent_cat")
        
        # 1. Cálculo de Cash histórico (para el ratio)
        balance_rows = db.query(
            models.Transaction.type,
            func.sum(models.Transaction.amount).label("total")
        ).filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.is_paid == True
        ).group_by(models.Transaction.type).all()
        
        totals = {r.type: float(r.total or 0) for r in balance_rows}
        cash = totals.get(models.TransactionType.income, 0) - \
               totals.get(models.TransactionType.expense, 0) - \
               totals.get(models.TransactionType.invest, 0)

        # 2. Query para el Treemap
        query = db.query(
            ParentCategory.name.label("parent_name"),
            models.Category.name.label("sub_name"),
            models.Transaction.description.label("description"), # <-- Añadimos descripción
            func.sum(models.Transaction.amount).label("value")
        ).join(models.Transaction, models.Category.id == models.Transaction.category_id)\
         .outerjoin(ParentCategory, models.Category.parent_id == ParentCategory.id)\
         .filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.type == models.TransactionType.invest,
            models.Transaction.is_paid == True,
            extract('year', models.Transaction.date) == year
        )

        if month:
            query = query.filter(extract('month', models.Transaction.date) == month)

        # Agrupamos también por descripción para no perder el detalle
        results = query.group_by(ParentCategory.name, models.Category.name, models.Transaction.description).all()

        data_map = {}
        total_invested = 0
        
        for r in results:
            p_name = r.parent_name or "Otros"
            sub_name = r.sub_name or "Sin Categoría"
            desc = r.description or "Sin descripción"
            val = float(r.value or 0)
            total_invested += val

            if p_name not in data_map:
                data_map[p_name] = {"name": p_name, "children": {}, "value": 0}
            
            data_map[p_name]["value"] += val
            
            # Agrupamos por Subcategoría (Nivel 1)
            if sub_name not in data_map[p_name]["children"]:
                data_map[p_name]["children"][sub_name] = {"name": sub_name, "children": [], "value": 0}
            
            data_map[p_name]["children"][sub_name]["value"] += val
            # Añadimos la descripción como hijo (Nivel 2)
            data_map[p_name]["children"][sub_name]["children"].append({
                "name": desc,
                "value": val
            })

        # Convertimos los diccionarios de hijos en listas para ECharts
        final_allocation = []
        for p_key, p_val in data_map.items():
            p_val["children"] = list(p_val["children"].values())
            final_allocation.append(p_val)

        return {
            "cash_ratio": {
                "invested": round(total_invested, 2),
                "cash": round(max(0, cash), 2)
            },
            "allocation": final_allocation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/summary", response_model=schemas.TransactionStatsResponse)
def get_transaction_summary(year: int = None, db: Session = Depends(get_db)):
    """Obtiene resumen de ingresos, gastos e inversión filtrado opcionalmente por año"""
    try:
        query = db.query(models.Transaction).filter(
            models.Transaction.user_id == USER_ID_MOCK,
            models.Transaction.is_paid == True
        )
        
        # Si se proporciona año, filtramos por la fecha de la transacción
        if year:
            query = query.filter(extract('year', models.Transaction.date) == year)
            
        transactions = query.all()
        
        # Cálculos de totales
        total_income = sum(t.amount for t in transactions if t.type == models.TransactionType.income)
        total_expense = sum(t.amount for t in transactions if t.type == models.TransactionType.expense)
        total_invest = sum(t.amount for t in transactions if t.type == models.TransactionType.invest)
        
        # Conteos de transacciones
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
            detail=f"Error al calcular estadísticas: {str(e)}"
        )
@router.get("/equity/evolution")
def get_equity_evolution(db: Session = Depends(get_db)):
    """Histórico mensual: Efectivo acumulado vs Inversión acumulada"""
    try:
        # Agrupamos por mes y calculamos el cambio neto de efectivo y de inversión
        rows = db.query(
            extract('year', models.Transaction.date).label("year"),
            extract('month', models.Transaction.date).label("month"),
            # Lo que entra/sale de la caja (Efectivo)
            func.sum(
                case(
                    (models.Transaction.type == models.TransactionType.income, models.Transaction.amount),
                    (models.Transaction.type == models.TransactionType.expense, -models.Transaction.amount),
                    (models.Transaction.type == models.TransactionType.invest, -models.Transaction.amount), # La inversión "sale" de la caja
                    else_=0
                )
            ).label("cash_change"),
            # Lo que entra en la cartera de inversión
            func.sum(
                case(
                    (models.Transaction.type == models.TransactionType.invest, models.Transaction.amount),
                    else_=0
                )
            ).label("invest_change")
        ).filter(
            models.Transaction.user_id == USER_ID_MOCK, 
            models.Transaction.is_paid == True
        ).group_by("year", "month").order_by("year", "month").all()

        history = []
        cum_cash = 0
        cum_invest = 0
        
        for r in rows:
            cum_cash += float(r.cash_change or 0)
            cum_invest += float(r.invest_change or 0)
            
            history.append({
                "date": f"{int(r.year)}-{str(int(r.month)).zfill(2)}",
                "cash": round(cum_cash, 2),
                "invested": round(cum_invest, 2),
                "total": round(cum_cash + cum_invest, 2)
            })
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT 2: Sunburst de Inversiones ---
@router.get("/equity/asset-types")
def get_asset_type_distribution(db: Session = Depends(get_db)):
    """Devuelve datos jerárquicos: Categoría (ETF/Crypto) -> Activo (Descripción)"""
    try:
        # Agrupamos por la categoría y la descripción para obtener el detalle del activo
        results = db.query(
            models.Category.name.label("cat_name"),
            models.Transaction.description.label("asset_name"),
            func.sum(models.Transaction.amount).label("total")
        ).join(models.Transaction, models.Category.id == models.Transaction.category_id)\
         .filter(
             models.Transaction.user_id == USER_ID_MOCK,
             models.Transaction.type == models.TransactionType.invest,
             models.Transaction.is_paid == True
         ).group_by(models.Category.name, models.Transaction.description).all()

        # Construimos el árbol para el Sunburst
        hierarchy = {}
        for r in results:
            cat = r.cat_name
            if cat not in hierarchy:
                hierarchy[cat] = {"name": cat, "children": []}
            
            hierarchy[cat]["children"].append({
                "name": r.asset_name or "Sin nombre",
                "value": float(r.total)
            })

        return list(hierarchy.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))