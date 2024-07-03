import re
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from sqlalchemy.orm import validates
from flask_login import UserMixin
from app import db


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


@dataclass
class User(UserMixin, db.Model):
    """user table"""

    id: int
    email: str
    username: str
    last_login: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime())
    status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.inactive)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime())

    def __repr__(self) -> str:
        return f"{self.username}"

    def __str__(self) -> str:
        return f"username: {self.username}, email: {self.email}"

    @validates("username")
    def validate_username(self, key, username):
        "validate username: unique and length"
        if not username:
            raise AssertionError("No username provided")
        if User.query.filter(User.username == username).first():
            raise AssertionError("phone number is already in use")
        if len(username) < 5 or len(username) > 20:
            raise AssertionError("Username must be between 5 and 20 characters")
        return username

    @validates("email")
    def validate_email(self, key, email):
        """validate user email"""
        if not email:
            raise AssertionError("No email provided")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not an email address")
        if User.query.filter(User.email == email).first():
            raise AssertionError("email address is already in use")
        return email

    def create(self, **kwargs):
        """create user object in the db"""
        try:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()

            return user
        except Exception as e:
            db.session.rollback()
            return None, f"500_error: {e.args[0]}"

    def get(self, query):
        """query user using username/id
        :return User or None"""
        user = User.query.filter((User.id == query) | (User.username == query)).first()
        
        return user

    def update(self, id, **updates):
        """update user object in the db"""
        try:
            user = User.query.filter(User.id == id).first()
            if not user:
                return None
            
            user = User.query.filter_by(id=id).update(
                    updates, synchronize_session="fetch"
                )
            db.session.commit()
            
            return user
        except Exception as e:
            db.session.rollback()
            return None, f"500_error: {e.args[0]}"
        
    def delete(self, id):
        """delete user
        :return: 0 or 1 - number of row deleted"""
        try:
            user = User.query.filter_by(id=id).first()
            if not user:
                return None, "404_user_not_found"
            user = User.query.filter_by(id=id).delete()
        except Exception as e:
            return None, f"500_error: {e.args[0]}"
        else:
            return user, "200_user_deleted"
