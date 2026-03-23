import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.repo.wordpress.dynamic_content import DynamicContentRepository
from app.schema.wordpress.signals import SignalCreate, SignalUpdate
from app.schema.wordpress.trading_tools import TradingToolCreate
from app.schema.wordpress.books import BookCreate, BookUpdate

async def verify_dynamic_content():
    print("Starting verification script...", flush=True)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        repo = DynamicContentRepository(session)
        user_id = 1  # Assuming admin user ID is 1

        # 1. Test Signals
        print("Testing Signals...", flush=True)
        signal_data = SignalCreate(
            title="Test EURUSD Buy",
            instrument="EURUSD",
            signal_type="vip",
            entry="1.0850",
            sl="1.0800",
            tp1="1.0900",
            tp2="1.0950"
        )
        print("Calling create_signal...", flush=True)
        new_signal = await repo.create_signal(user_id, signal_data)
        print(f"Created Signal ID: {new_signal.id}", flush=True)

        # Update test
        print(f"Updating Signal ID: {new_signal.id}...", flush=True)
        updated_signal = await repo.update_signal(new_signal.id, SignalUpdate(title="Test EURUSD Buy - Updated", sl="1.0790"))
        print(f"Updated Signal title: {updated_signal.title}, SL: {updated_signal.sl}", flush=True)

        print("Calling get_signals...", flush=True)
        signals = await repo.get_signals(limit=5)
        print(f"Total Signals found: {len(signals)}", flush=True)
        for s in signals:
            print(f"- {s.title} ({s.instrument}): {s.signal_type}", flush=True)

        # ... (Trading Tools part unchanged)

        # 3. Test Books
        print("\nTesting Books...", flush=True)
        book_data = BookCreate(
            title="Forex 101",
            is_free=True,
            description="Basics for beginners",
            download_url="https://example.com/books/101.pdf"
        )
        print("Calling create_book...", flush=True)
        new_book = await repo.create_book(user_id, book_data)
        print(f"Created Book ID: {new_book.id}", flush=True)

        # Update test
        print(f"Updating Book ID: {new_book.id}...", flush=True)
        updated_book = await repo.update_book(new_book.id, BookUpdate(title="Forex 101 - Updated"))
        print(f"Updated Book title: {updated_book.title}", flush=True)

        # Delete test
        print(f"Deleting Book ID: {new_book.id}...", flush=True)
        deleted = await repo.delete_book(new_book.id)
        print(f"Deleted Book success: {deleted}", flush=True)

        print("Calling get_books...", flush=True)
        books = await repo.get_books(limit=5)
# ...rest of file

        # 4. Test Videos
        print("\nTesting Videos...", flush=True)
        print("Calling create_trading_video...", flush=True)
        new_video = await repo.create_trading_video(user_id, "Winning Strategy", "dQw4w9WgXcQ", "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg")
        print(f"Created Video: {new_video['title']}", flush=True)

        print("Calling get_trading_videos...", flush=True)
        videos = await repo.get_trading_videos(limit=5)
        print(f"Total Videos found: {len(videos)}", flush=True)
        for v in videos:
            print(f"- {v['title']} (ID: {v['id']})", flush=True)

if __name__ == "__main__":
    asyncio.run(verify_dynamic_content())
