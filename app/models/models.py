from sqlalchemy import Column, DateTime, Float, String, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currencies'

    name = Column(String, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    rate = Column(Float, nullable=False)
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Currency(name='{self.name}', code='{self.code}', rate={self.rate})>"
