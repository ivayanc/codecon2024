from typing import Optional

import sqlalchemy as sa

from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from database.base import Base

from configuration import ADMIN_PANEL_PAGE_SIZE


class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True)
    username: Mapped[Optional[str]]
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date]
    phone_number: Mapped[Optional[str]]
    city: Mapped[str]
    street: Mapped[str]
    home_number: Mapped[int]
    flat_number: Mapped[int]
    is_banned: Mapped[bool] = mapped_column(default=False)
    is_volunteer: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'< Username: {self.username}, Telegram Id: {self.telegram_id} >'


class UserView(ModelView):
    column_list = ('telegram_id', 'username', 'first_name', 'last_name', 'birth_date',
                   'phone_number', 'city', 'street', 'home_number',
                   'flat_number', 'is_banned', 'is_volunteer', 'is_admin')
    form_columns = ('telegram_id', 'username', 'phone_number', 'is_banned', 'is_volunteer')
    column_searchable_list = ['telegram_id', 'username', 'first_name', 'last_name',
                              'birth_date', 'phone_number', 'city', 'street',
                              'home_number', 'flat_number']
    column_filters = ['is_banned', 'is_volunteer', 'is_admin']
    page_size = ADMIN_PANEL_PAGE_SIZE
