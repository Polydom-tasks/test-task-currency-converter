from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.db import SessionLocal
from app.models.models import Currency
from app.services.currency_service import CurrencyService

router = APIRouter()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@router.post("/update-rates", status_code=200)
async def update_exchange_rates(db: AsyncSession = Depends(get_db)):
    try:
        await CurrencyService.update_currency_rates(session=db)
        return {"message": "Exchange rates updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/last-update", status_code=200)
async def last_update(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(func.max(Currency.updated_at)))
        last_update_time = result.scalar_one_or_none()
        if last_update_time:
            return {"last_update": last_update_time}
        else:
            return {"message": "No update information available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/convert", status_code=200)
async def convert_currency(
    source: str = Query(..., description="Source currency code"),
    target: str = Query(..., description="Target currency code"),
    amount: float = Query(..., description="Amount to convert"),
    db: AsyncSession = Depends(get_db)
):
    try:
        async with db.begin():
            stmt = select(Currency).where(Currency.code.in_([source, target]))
            result = await db.execute(stmt)
            currencies = result.scalars().all()

            if len(currencies) < 2:
                raise HTTPException(status_code=404, detail="One or both currencies not found")

            source_currency = next((c for c in currencies if c.code == source), None)
            target_currency = next((c for c in currencies if c.code == target), None)

            converted_amount = (amount / source_currency.rate) * target_currency.rate

            return {
                "source": source,
                "target": target,
                "amount": amount,
                "converted_amount": converted_amount
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
