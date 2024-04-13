from typing import Optional

from datetime import date

import sqlalchemy as sa

from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database.base import Base

from configuration import ADMIN_PANEL_PAGE_SIZE


class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True)
    username: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    birthday_date: Mapped[Optional[date]]
    region: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    street: Mapped[Optional[str]]
    house_number: Mapped[Optional[str]]
    flat_number: Mapped[Optional[str]]
    is_banned: Mapped[bool] = mapped_column(default=False)
    is_volunteer: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'< Username: {self.username}, Telegram Id: {self.telegram_id} >'


class UserView(ModelView):
    column_list = ('telegram_id', 'username', 'phone_number', 'is_banned', 'is_volunteer', 'is_admin')
    form_columns = ('telegram_id', 'username', 'phone_number', 'is_banned', 'is_volunteer')
    column_searchable_list = ['telegram_id', 'username', 'phone_number']
    column_filters = ['is_banned', 'is_volunteer', 'is_admin']
    page_size = ADMIN_PANEL_PAGE_SIZE
