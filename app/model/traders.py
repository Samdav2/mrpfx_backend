from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String

class Trader(SQLModel, table=True):
    """Database model for MT5 Managers/Traders."""
    __tablename__ = "8jH_traders"

    id: Optional[int] = Field(default=None, primary_key=True)
    trader_id: str = Field(sa_column=Column(String(191), unique=True, index=True, nullable=False), description="String identifier like 'managerC'")
    name: str = Field(description="Display name, e.g., 'Elite Trader C'")
    type: str = Field(default="Aggressive", description="Trading style type")
    strategy: str = Field(description="Description of the trading strategy")
    description: Optional[str] = Field(default=None, description="Detailed strategy description")
    profit_factor: str = Field(default="0.00", description="e.g., '2.14'")
    avg_trade_duration: str = Field(default="0", description="e.g., '4.2 Days'")
    best_trade: str = Field(default="$0", description="e.g., '+$1,450'")
    worst_trade: str = Field(default="$0", description="e.g., '-$320'")

class TraderPerformance(SQLModel, table=True):
    """Database model for monthly trader performance records."""
    __tablename__ = "8jH_trader_performance"

    id: Optional[int] = Field(default=None, primary_key=True)
    trader_id: str = Field(foreign_key="8jH_traders.trader_id", index=True, max_length=191)
    month: str = Field(description="Formatted month string, e.g., 'February 2026'")
    date_timestamp: datetime = Field(description="Used for sorting descending")
    win_rate: str = Field(description="e.g., '72%'")
    monthly_roi: str = Field(description="e.g., '15-25%'")
    max_drawdown: str = Field(description="e.g., '15%'")
    total_trades: str = Field(description="e.g., '4,850'")
