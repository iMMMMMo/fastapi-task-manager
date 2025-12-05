from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
oauth2_scheme = HTTPBearer()


@router.post("/register", response_model=UserRead, status_code=201)
def register_user(data: UserCreate, db: Session = Depends(get_session)):
    user_exists = select(User).where(User.email == data.email)
    if db.exec(user_exists).first():
        raise HTTPException(status_code=400, detail="Email already registered.")

    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    query = select(User).where(User.email == form_data.username)
    user = db.exec(query).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})
    return Token(access_token=access, refresh_token=refresh)


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_session)
):
    payload = decode_token(token.credentials)
    if token.scheme.lower() != "bearer":
     raise HTTPException(status_code=401, detail="Invalid auth scheme.")

    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user_id = payload.get("sub")
    user = db.get(User, int(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
