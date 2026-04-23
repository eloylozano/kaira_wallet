from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

import models, schemas
from database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    redirect_slashes=True
)

USER_ID_MOCK = 1  # ⚠️ luego cámbialo por auth real


# =========================================================
# 📌 GET ALL CATEGORIES (árbol completo)
# =========================================================
@router.get("/", response_model=List[schemas.CategoryWithSubcategories])
def get_categories(db: Session = Depends(get_db)):
    try:
        categories = (
            db.query(models.Category)
            .options(joinedload(models.Category.subcategories))
            .filter(models.Category.user_id == USER_ID_MOCK)
            .filter(models.Category.parent_id == None)
            .all()
        )

        for cat in categories:
            cat.subcategories = [
                sub for sub in cat.subcategories
                if sub.user_id == USER_ID_MOCK
            ]

        return categories

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# 📌 GET PREDEFINED (opcional)
# =========================================================
@router.get("/predefined", response_model=List[schemas.CategoryWithSubcategories])
def get_predefined_categories(
    transaction_type: Optional[schemas.TransactionType] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Category).filter(
        models.Category.is_predefined == True,
        models.Category.parent_id == None
    )

    if transaction_type:
        query = query.filter(models.Category.transaction_type == transaction_type)

    return query.all()


# =========================================================
# 📌 CREATE CATEGORY (padre o subcategoría)
# =========================================================
@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    try:
        # validar parent
        if category.parent_id is not None:
            parent = db.query(models.Category).filter(
                models.Category.id == category.parent_id,
                models.Category.user_id == USER_ID_MOCK
            ).first()

            if not parent:
                raise HTTPException(status_code=404, detail="Parent category not found")

        db_category = models.Category(
            **category.model_dump(),
            user_id=USER_ID_MOCK,
            is_predefined=False
        )

        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return db_category

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# 📌 UPDATE CATEGORY
# =========================================================
@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category_update: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    try:
        db_category = db.query(models.Category).filter(
            models.Category.id == category_id,
            models.Category.user_id == USER_ID_MOCK
        ).first()

        if not db_category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

        # 🚫 evitar self parent
        if category_update.parent_id == category_id:
            raise HTTPException(
                status_code=400,
                detail="Una categoría no puede ser su propio padre"
            )

        # 🚫 validar parent existe (IMPORTANTE también en update)
        if category_update.parent_id is not None:
            parent = db.query(models.Category).filter(
                models.Category.id == category_update.parent_id,
                models.Category.user_id == USER_ID_MOCK
            ).first()

            if not parent:
                raise HTTPException(status_code=404, detail="Parent category not found")

        for key, value in category_update.model_dump().items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)

        return db_category

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# 📌 DELETE CATEGORY
# =========================================================
from sqlalchemy import exists

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):

    db_category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == USER_ID_MOCK
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    # 🚨 comprobar movimientos asociados
    has_transactions = db.query(
        db.query(models.Transaction)
        .filter(models.Transaction.category_id == category_id)
        .exists()
    ).scalar()

    if has_transactions:
        raise HTTPException(
            status_code=409,
            detail="No puedes borrar esta categoría porque tiene movimientos asociados."
        )

    try:
        db.delete(db_category)
        db.commit()

        return {
            "message": f"Categoría {category_id} eliminada correctamente"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al borrar: {str(e)}"
        )