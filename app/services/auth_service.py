from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import BadRequestException, PermissionDeniedException, NotFoundException, UnauthorizedException
from app.repositories.auth_repo import AuthRepository


class AuthService:

    @staticmethod
    def register(db: Session, data: UserCreate) -> User:
        existing = AuthRepository.get_by_email(db, data.email)
        if existing:
            raise BadRequestException("Email already registered")
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password)
        )
        return AuthRepository.create(db, user)

    @staticmethod
    def login(db: Session, form_data: OAuth2PasswordRequestForm) -> dict:
        user = AuthRepository.get_by_email(db, form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")
        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        return {"access_token": access, "refresh_token": refresh}

    @staticmethod
    def get_user_from_token(db: Session, token: HTTPAuthorizationCredentials) -> User:
        if token.scheme.lower() != "bearer":
            raise UnauthorizedException("Invalid authentication credentials")
        payload = decode_token(token.credentials)
        if not payload or payload.get("type") != "access":
            raise UnauthorizedException("Invalid authentication credentials")
        user_id = payload.get("sub")
        return AuthRepository.get_by_id(db, int(user_id))