from fastapi import APIRouter, Response

from src.application.requests.personal import *

router = APIRouter(
    prefix="/api/v1/personal",
    tags=["user"],
    responses={404: {'message': 'Not found'}, 500: {'message': 'Server error'}},
)


@router.post('/auth/login')
def login(request: LoginRequest, response: Response):
    pass


@router.post('/auth/registration')
def registration(request: RegistrationRequest, response: Response):
    pass


@router.get('/profile')
def profile():
    pass


@router.post('/profile')
def profile_save(request: ProfileRequest):
    pass


@router.get('/profile/pairs')
def pairs():
    pass


@router.post('/profile/pairs')
def pairs_save(request: PairsRequest):
    pass


@router.post('/profile/reset_password')
def reset_password(request: ResetPasswordRequest):
    pass


if __name__ == '__main__':
    pass
