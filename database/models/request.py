from typing import Optional

import sqlalchemy as sa

from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from database.base import Base
from bot.utils.enums import RequestStatus, RequestType

from configuration import ADMIN_PANEL_PAGE_SIZE


class Request(Base):
    __tablename__ = 'request'
    request_id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True)
    region = relationship("Region")
    region_id: Mapped[int] = mapped_column(sa.ForeignKey("region.region_id"))
    user_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey("users.telegram_id"))
    user = relationship("User", foreign_keys=[user_id])
    type: Mapped[RequestType]
    city: Mapped[Optional[str]]
    street: Mapped[Optional[str]]
    home_number: Mapped[Optional[str]]
    flat_number: Mapped[Optional[str]]
    contact_first_name: Mapped[Optional[str]]
    contact_last_name: Mapped[Optional[str]]
    contact_phone_number: Mapped[Optional[str]]
    request_text: Mapped[str]
    volunteer_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, sa.ForeignKey("users.telegram_id"))
    volunteer = relationship("User", foreign_keys=[volunteer_id])
    request_status: Mapped[RequestStatus]
    request_date: Mapped[datetime]
    request_delivery_date: Mapped[Optional[datetime]]
    is_delivery: Mapped[bool] = mapped_column(sa.Boolean(), default=False)

    def __repr__(self):
        return f'< Request: {self.request_id}, User: {self.user_id} ' \
               f'Volunteer: {self.volunteer_id} Region: {self.region_id}>'


class RequestView(ModelView):
    column_list = ('request_id', 'region_id', 'user_id', 'city', 'street', 'home_number',
                   'flat_number', 'contact_first_name', 'contact_last_name', 'contact_phone_number', 'request_text',
                   'volunteer_id', 'request_status',
                   'request_date', 'request_delivery_date')
    form_columns = ('request_id', 'region_id', 'user_id', 'city', 'street', 'home_number',
                    'flat_number', 'contact_first_name', 'contact_last_name',
                    'contact_phone_number', 'request_text', 'volunteer_id', 'request_status',
                    'request_date', 'request_delivery_date')
    column_searchable_list = ['request_id', 'region_id', 'user_id', 'city', 'street', 'home_number',
                              'flat_number', 'contact_first_name', 'contact_last_name',
                              'contact_phone_number', 'request_text', 'volunteer_id', 'request_status']
    column_filters = ['request_status', 'request_date', 'request_delivery_date']
    page_size = ADMIN_PANEL_PAGE_SIZE
