from functools import wraps

from src.infrastructure.database.session import session


def transaction(coro):
    """This decorator should be used with all coroutines
    that want's access the database for saving a new data.
    """

    @wraps(coro)
    async def inner(*args, **kwargs):
        result = await coro(*args, **kwargs)
        current_session = args[0].session if args[0].session is not None else session
        await current_session.commit()
        return result
        # try:
        #     result = await coro(*args, **kwargs)
        #     await session.commit()
        #     return result
        # except BaseException:
        #     await session.rollback()
        # finally:
        #     await session.close()

    return inner
