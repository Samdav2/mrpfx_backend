import asyncio
from datetime import datetime, timedelta
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.traders import Trader, TraderPerformance

async def seed_traders():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        print("Seeding traders...")

        traders = [
            Trader(
                trader_id="managerA",
                name="Master Trader A",
                type="Conservative",
                strategy="Low-risk algorithmic hedging with strict stop losses.",
                description="Master Trader A employs a highly conservative strategy focused on wealth preservation. Utilizing proprietary algorithmic hedging techniques, this manager aims for consistent, low-volatility returns. Every position is strictly protected by hard stop losses, ensuring drawdowns remain minimal. Ideal for capital preservation.",
                profit_factor="2.14",
                avg_trade_duration="4.2 Days",
                best_trade="+$1,450",
                worst_trade="-$320"
            ),
            Trader(
                trader_id="managerB",
                name="Pro Trader B",
                type="Balanced",
                strategy="Intraday trend following with dynamic position sizing.",
                description="Pro Trader B utilizes a balanced approach, capturing medium-term trends while managing risk dynamically. This strategy involves intraday trading, capitalizing on market momentum during peak volume hours. It offers a solid middle ground between steady growth and calculated risk-taking.",
                profit_factor="1.85",
                avg_trade_duration="1.5 Days",
                best_trade="+$2,800",
                worst_trade="-$950"
            ),
            Trader(
                trader_id="managerC",
                name="Elite Trader C",
                type="Aggressive",
                strategy="High-frequency scalping during volatile market sessions.",
                description="Elite Trader C is designed for investors seeking maximum growth. Employing aggressive, high-frequency scalping techniques, this manager targets short-term volatility bursts across major pairs and indices. While drawdowns are naturally higher, the potential for rapid portfolio expansion is significant.",
                profit_factor="1.65",
                avg_trade_duration="4 Hours",
                best_trade="+$5,200",
                worst_trade="-$1,800"
            )
        ]

        for t in traders:
            session.add(t)
        await session.commit()

        base_date = datetime(2026, 2, 1)

        # Performance for A
        print("Seeding performance for A...")
        for i in range(12):
            date = base_date - timedelta(days=30*i)
            perf = TraderPerformance(
                trader_id="managerA",
                month=date.strftime("%B %Y"),
                date_timestamp=date,
                win_rate=f"{85 - i}%",
                monthly_roi="4-6%",
                max_drawdown=f"{3 + i // 3}%",
                total_trades=str(1240 - i * 20)
            )
            session.add(perf)

        # Performance for B
        print("Seeding performance for B...")
        for i in range(12):
            date = base_date - timedelta(days=30*i)
            perf = TraderPerformance(
                trader_id="managerB",
                month=date.strftime("%B %Y"),
                date_timestamp=date,
                win_rate=f"{78 - i // 2}%",
                monthly_roi="8-12%",
                max_drawdown=f"{7 + i // 4}%",
                total_trades=str(3100 - i * 50)
            )
            session.add(perf)

        # Performance for C
        print("Seeding performance for C...")
        for i in range(12):
            date = base_date - timedelta(days=30*i)
            perf = TraderPerformance(
                trader_id="managerC",
                month=date.strftime("%B %Y"),
                date_timestamp=date,
                win_rate=f"{72 - i}%",
                monthly_roi="15-25%",
                max_drawdown=f"{15 + i // 3}%",
                total_trades=str(4850 - i * 100)
            )
            session.add(perf)

        await session.commit()
        print("Done seeding!")

if __name__ == "__main__":
    asyncio.run(seed_traders())
