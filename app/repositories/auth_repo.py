from sqlmodel import Session, select
from app.models.user import User
from app.core.exceptions import NotFoundException


class AuthRepository:

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    @staticmethod
    def create(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        user = db.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")
        return user