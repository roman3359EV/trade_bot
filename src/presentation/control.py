from fastapi import APIRouter, Response

from src.application.control.manual import Manual as ManualControl
from src.domain.personal.user_repository import UserRepository

router = APIRouter(
    prefix="/api/v1/control",
    tags=["ask"],
    responses={404: {'message': 'Not found'}, 500: {'message': 'Server error'}},
)


@router.get('/buy/{pair}')
async def buy(pair: str, user_id: int, response: Response):
    try:
        user = await UserRepository().get(user_id)
        control = ManualControl(user)
        await control.manual_buy(pair)
    except Exception as exception:
        response.status_code = 500
        return {
            'message': 'Server error',
            'detail': f"{exception}"
        }


@router.get('/sell')
async def sell(order_id: int, user_id: int, response: Response):
    # try:
        user = await UserRepository().get(user_id)
        control = ManualControl(user)
        await control.manual_sell(order_id)
    # except Exception as exception:
    #     response.status_code = 500
    #     return {
    #         'message': 'Server error',
    #         'detail': f"{exception}"
    #     }


if __name__ == '__main__':
    pass
