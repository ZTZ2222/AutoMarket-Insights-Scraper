import decimal
from fastapi import HTTPException, status
from sqlalchemy import Numeric, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class CarOrm(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    make_model: Mapped[str] = mapped_column(index=True)
    slug: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int] = mapped_column()
    price_usd: Mapped[decimal.Decimal] = mapped_column(Numeric(precision=10, scale=2))
    price_som: Mapped[decimal.Decimal] = mapped_column(Numeric(precision=10, scale=2))
    transmission: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column()
    body_type: Mapped[str] = mapped_column()
    engine_cap: Mapped[float] = mapped_column()
    engine_type: Mapped[str] = mapped_column()
    wheel_pos: Mapped[str] = mapped_column()
    mileage: Mapped[int] = mapped_column()
    city: Mapped[str] = mapped_column()
    car_link: Mapped[str] = mapped_column()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    async def find(cls, db_session: AsyncSession, slug: str):
        stmt = select(cls).where(cls.slug == slug)
        result = await db_session.execute(stmt)
        car = result.scalars().first()
        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "Product not found": f"There is no product for requested slug value : {slug}"
                },
            )
        else:
            return car
