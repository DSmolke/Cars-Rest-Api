from app.db.configuration import sa
from typing import Self
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(sa.Model):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(255))
    password = sa.Column(sa.String(255))
    email = sa.Column(sa.String(255))
    role = sa.Column(sa.String(10))
    active = sa.Column(sa.Boolean, default=False)

    def __init__(self, username: str, password: str, email: str, role: str):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.role = role

    def save_or_update(self) -> None:
        sa.session.add(self)
        sa.session.commit()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def as_dict(self):
        return {
            'username': self.username,
            'role': self.role,
            'active': self.active
        }

    @classmethod
    def find_by_username(cls, username: str) -> Self | None:
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> Self | None:
        return UserModel.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        return UserModel.query.filter_by(id=id_).first()
