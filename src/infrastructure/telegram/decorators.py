from functools import wraps


def session_close(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        await args[0].bot.session.close()

        return result

    return wrapper
