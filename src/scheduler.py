import asyncio
from asyncio import Task
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.domain.personal.user_repository import UserRepository
from src.infrastructure.database.session import async_engine, async_sessionmaker
from src.application.control.automatic import Automatic
from src.application.control.manual import Manual


# 1 task = 1 db session
async def automatic_task(semaphore, user):
    async with semaphore:
        print(1)
        session = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)()
        automatic_control = Automatic(user, session)
        await automatic_control.solve('BTC_USDT')
        await session.close()


async def manual_task(semaphore, user):
    async with semaphore:
        print(2)
        session = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)()
        manual_control = Manual(user, session)
        await manual_control.solve('BTC_USDT')
        await session.close()


async def solve() -> list[Task]:
    session = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)()
    repository = UserRepository(session)
    users = await repository.all()
    await session.close()
    tasks = []
    semaphore = asyncio.Semaphore(2)

    for user in users:
        tasks.append(asyncio.create_task(automatic_task(semaphore, user)))
        tasks.append(asyncio.create_task(manual_task(semaphore, user)))

    return tasks


async def async_main():
    tasks = await solve()
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=async_main, trigger='interval', minutes=1)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
