import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import settings
from app.models.models import Currency


class CurrencyService:
    @staticmethod
    async def update_currency_rates(session: AsyncSession):
        url = f"http://api.exchangeratesapi.io/v1/latest?access_key={settings.exchangeratesapi_token}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            rates = response.json().get('rates', {})

            async with session.begin():
                for code, rate in rates.items():
                    stmt = select(Currency).where(Currency.code == code)
                    result = await session.execute(stmt)
                    currency = result.scalars().first()
                    if currency:
                        currency.rate = rate
                    else:
                        new_currency = Currency(name=code, code=code, rate=rate)
                        session.add(new_currency)
                await session.commit()
