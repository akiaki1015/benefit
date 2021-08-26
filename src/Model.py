from sqlalchemy import (Column, String, DATETIME, Index, UniqueConstraint)
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class History(Base):
    __tablename__ = "History"
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    product_name = Column(String(255))
    balance = Column(String(255))  # 資産残高
    price = Column(String(255))  # 購入金額
    pl_price = Column(String(255))  # Profit and Loss => pl # 損益
    pl_rate = Column(String(255))  # Profit and Loss => pl # 損益率
    create_time = Column(DATETIME, nullable=False, server_default=func.now())
    __table_args__ = (Index('history_index', "create_time"),)