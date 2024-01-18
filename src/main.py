import uvicorn, asyncio
from fastapi import FastAPI

from src.presentation import control, personal

app = FastAPI()
app.include_router(control.router)
app.include_router(personal.router)

from src.domain.personal.user import User
from src.application.control.automatic import Automatic
from src.application.control.manual import Manual

if __name__ == '__main__':
    #user = User(id=4, telegram_id=203603083)
    #automatic = Automatic(user)
    #automatic = Manual(user)
    #asyncio.run(automatic.solve('BTC_USDT'))
    uvicorn.run(app, host="0.0.0.0", port=5050)
