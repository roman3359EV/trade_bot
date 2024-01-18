from pydantic import BaseModel
from typing import Union


class LoginRequest(BaseModel):
    login: str
    password: str


class RegistrationRequest(BaseModel):
    login: str
    password: str
    telegram_id: Union[int, None] = None


class ProfileRequest(BaseModel):
    token: str
    login: str
    is_active: bool
    telegram_id: Union[int, None] = None


class PairsRequest(BaseModel):
    token: str
    pairs: Union[dict, None] = None


class ResetPasswordRequest(BaseModel):
    token: str
    password: str
    new_password: str
    confirm_password: str


__all__ = ['LoginRequest', 'RegistrationRequest', 'ProfileRequest', 'PairsRequest', 'ResetPasswordRequest']