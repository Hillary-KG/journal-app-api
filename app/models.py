import re
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from sqlalchemy.orm import validates, Mapped
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
    journal_entries: Mapped["JournalEntry"]

    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime())
    status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.inactive)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime())
    categories = db.relationship("Category", backref="users", lazy=True)
    journal_entries = db.relationship("JournalEntry", backref="users", lazy=True)

    def __repr__(self) -> str:
        return f"{self.username}: {self.email}"

    def __str__(self) -> str:
        return f"username: {self.username}, email: {self.email}"

    @validates("username")
    def validate_username(self, key, username):
        "validate username: unique and length"
        if not username:
            raise AssertionError("No username provided")
        if User.query.filter(User.username == username).first():
            raise AssertionError("username is taken")
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

            return user, "success"
        except Exception as e:
            db.session.rollback()
            return None, f"{e.args[0]}"

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
                return None, "no updates"

            user = User.query.filter_by(id=id).update(
                updates, synchronize_session="fetch"
            )
            db.session.commit()

            return user, "success"
        except Exception as e:
            db.session.rollback()
            return None, {e.args[0]}

    def delete(self, id):
        """delete user
        :return: 0 or 1 - number of row deleted"""
        try:
            user = User.query.filter_by(id=id).first()
            if not user:
                return None, "404_user_not_found"
            user = User.query.filter_by(id=id).delete()
        except Exception as e:
            return None, e.args[0]
        else:
            return user, "200_user_deleted"

@dataclass
class Category(db.Model):
    """this class describes a journal category object"""

    __tablename__ = "category"
    id: int
    name: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime())
    journal_entries = db.relationship("JournalEntry", backref="category", lazy=True)

    def __str__(self):
        return f"{self.name}"

    def create(self, **kwargs):
        """Create category"""
        try:
            kwargs["created_at"] = datetime.now()
            category = Category(**kwargs)
            db.session.add(category)
            db.session.flush()
            if not category.id:
                return None, "400_error"
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return None, e.args[0]
        else:
            return category, "201_created"

    def update_category(self, user_id, **kwargs):
        """Update category"""
        try:
            category = Category.query.filter_by(id=kwargs.get("id"), user_id=user_id).first()
            if not category:
                return None, "404_not_found"
            kwargs["updated_at"] = datetime.now()
            updated = Category.query.filter_by(id=kwargs.get("id"),user_id=user_id).update(
                kwargs, synchronize_session="fetch"
            )
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return None, e.args[0]
        else:
            return category, "200_updated"

    def delete_category(self, id, user_id):
        """Delete category"""
        try:
            category = Category.query.filter_by(id=id, user_id=user_id).first()
            if not category:
                return None, "404_category_not_found"
            category = Category.query.filter_by(id=id, user_id=user_id).delete()
            db.session.commit()
        except Exception as e:
            return None, e.args[0]
        else:
            return category, "200_deleted"

    def get_category(self, user_id, id):
        """Fetch category"""
        try:
            category = Category.query.filter_by(id=id, user_id=user_id).first()
            if not category:
                return None, "404_not_found"
        except Exception as e:
            return None, e.args[0]
        else:
            return category, "200_ok"

    def get_categories(self, user_id):
        """Fetch categories"""
        try:
            categories = Category.query.filter_by(user_id=user_id).all()
            if not categories:
                return None, "404_no_found"
        except Exception as e:
            return None, e.args[0]
        else:
            return categories, "200_ok"

@dataclass
class JournalEntry(db.Model):
    """this class describes a journal entry object"""

    __tablename__ = "journal_entry"
    id: int
    user_id: int
    category_id: int
    entry: str
    created_at: datetime
    updated_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime())

    def __str__(self):
        return f"{self.id}: {self.entry[:15]} ..."

    def create(self, **kwargs):
        """Create journal entry"""
        try:
            kwargs["created_at"] = datetime.now()
            entry = JournalEntry(**kwargs)
            db.session.add(entry)
            db.session.flush()
            if not entry.id:
                return None, "400_error: entry creation failed"
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return None, e.args[0]
        else:
            return entry, "201_journal_entry_created"

    def update_journal_entry(self, user_id, **kwargs):
        """Update journal entry"""
        try:
            entry = JournalEntry.query.filter_by(
                id=kwargs.get("id"), user_id=user_id
            ).first()
            if not entry:
                return None, "404_journal_entry_not_found"
            kwargs["updated_at"] = datetime.now()
            entry = JournalEntry.query.filter_by(id=kwargs.get("id"), user_id=user_id).update(
                kwargs, synchronize_session="fetch"
            )
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return None, e.args[0]
        else:
            return entry, "200_journal_entry_updated"

    def delete_journal_entry(self, user_id, id):
        """Delete journal entry"""
        try:
            deleted = JournalEntry.query.filter_by(id=id, user_id=user_id).delete()
            db.session.commit()
        except Exception as e:
            return None, e.args[0]
        else:
            return deleted, "200_journal_entry_deleted"

    def get_journal_entry(self, user_id, id):
        """Fetch journal entry"""
        try:
            entry = JournalEntry.query.filter_by(id=id, user_id=user_id).first()
            if not entry:
                return None, "404_journal_entry_not_found"
        except Exception as e:
            return None, e.args[0]
        else:
            return entry, "200_journal_entry_found"

    def get_journal_entries(self, user_id):
        """Fetch all user journal entries"""
        try:
            entries = JournalEntry.query.filter_by(user_id=user_id).all()
            if not entries:
                return None, "404_journals_not_found"
        except Exception as e:
            return None, e.args[0]
        else:
            return entries, "200_journal_entries_found"
