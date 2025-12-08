from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = HTTPBearer()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    data: UserCreate, 
    db: Session = Depends(get_session)
):
    return AuthService.register(db, data)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_session)
):
    tokens = AuthService.login(db, form_data)
    return Token(access_token=tokens["access_token"], refresh_token=tokens["refresh_token"])


@router.get("/me", response_model=UserRead)
def read_me(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), 
    db: Session = Depends(get_session)
):
    return AuthService.get_user_from_token(db, token)


def get_current_user(
    token = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
) -> User:
    return AuthService.get_user_from_token(db, token)
