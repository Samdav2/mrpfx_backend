import asyncio
from sqlmodel import SQLModel, select
from datetime import datetime, timedelta

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.traders import Trader, TraderPerformance

async def seed_traders():
    # Attempt to create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Check if managerC exists
        stmt = select(Trader).where(Trader.trader_id == "managerC")
        result = await session.exec(stmt)
        existing_trader = result.first()

        if not existing_trader:
            print("Seeding managerC...")
            trader = Trader(
                trader_id="managerC",
                name="Elite Trader C",
                type="Aggressive",
                strategy="High-frequency scalping during volatile market sessions."
            )
            session.add(trader)
            await session.commit()
        else:
            print("managerC already exists.")
            trader = existing_trader

        # Check performances
        perf_stmt = select(TraderPerformance).where(TraderPerformance.trader_id == "managerC")
        perf_result = await session.exec(perf_stmt)
        existing_perfs = perf_result.all()

        if not existing_perfs:
            print("Seeding performance records for managerC...")

            # Start from this month and go back 11 months
            base_date = datetime(2026, 2, 1)  # Using Feb 2026 based on requirements

            # Generating mock data similar to what was requested
            mock_data = [
                {"win_rate": "72%", "monthly_roi": "15-25%", "max_drawdown": "15%", "total_trades": "4,850"},
                {"win_rate": "68%", "monthly_roi": "10-18%", "max_drawdown": "18%", "total_trades": "4,120"},
                {"win_rate": "75%", "monthly_roi": "18-30%", "max_drawdown": "12%", "total_trades": "5,100"},
                {"win_rate": "70%", "monthly_roi": "12-20%", "max_drawdown": "16%", "total_trades": "4,400"},
                {"win_rate": "74%", "monthly_roi": "20-28%", "max_drawdown": "14%", "total_trades": "4,950"},
                {"win_rate": "65%", "monthly_roi": "8-15%", "max_drawdown": "20%", "total_trades": "3,800"},
                {"win_rate": "71%", "monthly_roi": "14-22%", "max_drawdown": "15%", "total_trades": "4,350"},
                {"win_rate": "76%", "monthly_roi": "22-35%", "max_drawdown": "11%", "total_trades": "5,300"},
                {"win_rate": "69%", "monthly_roi": "11-19%", "max_drawdown": "17%", "total_trades": "4,250"},
                {"win_rate": "73%", "monthly_roi": "16-24%", "max_drawdown": "13%", "total_trades": "4,700"},
                {"win_rate": "67%", "monthly_roi": "9-16%", "max_drawdown": "19%", "total_trades": "4,050"},
                {"win_rate": "78%", "monthly_roi": "25-40%", "max_drawdown": "10%", "total_trades": "5,600"}
            ]

            for i in range(12):
                # Subtract months (approximate by 30 days)
                # Using relativedelta from dateutil would be better, but we do basic math for month
                target_month = (base_date.month - i - 1) % 12 + 1
                target_year = base_date.year + ((base_date.month - i - 1) // 12)

                # A proper datetime timestamp for sorting
                current_date = datetime(target_year, target_month, 1)
                month_str = current_date.strftime("%B %Y")

                data = mock_data[i]

                perf = TraderPerformance(
                    trader_id="managerC",
                    month=month_str,
                    date_timestamp=current_date,
                    win_rate=data["win_rate"],
                    monthly_roi=data["monthly_roi"],
                    max_drawdown=data["max_drawdown"],
                    total_trades=data["total_trades"]
                )
                session.add(perf)

            await session.commit()
            print("Successfully seeded 12 months of performance data!")
        else:
            print(f"Found {len(existing_perfs)} existing performance records.")

if __name__ == "__main__":
    asyncio.run(seed_traders())
