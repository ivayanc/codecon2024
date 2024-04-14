from typing import Optional

import sqlalchemy as sa

from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from database.base import Base
from bot.utils.enums import EvacuationRequestStatus

from configuration import ADMIN_PANEL_PAGE_SIZE


class EvacuationRequest(Base):
    __tablename__ = 'evacuation_request'
    request_id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True)
    region = relationship("Region")
    region_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("region.region_id"))
    user_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey("users.telegram_id"))
    user = relationship("User", foreign_keys=[user_id])
    city: Mapped[str]
    street: Mapped[str]
    home_number: Mapped[str]
    flat_number: Mapped[str]
    contact_first_name: Mapped[Optional[str]]
    contact_last_name: Mapped[Optional[str]]
    contact_phone_number: Mapped[Optional[str]]
    evacuation_qnt: Mapped[int] = mapped_column(default=1)
    any_special_needs: Mapped[bool] = mapped_column(sa.Boolean(), default=False)
    special_needs: Mapped[Optional[str]]
    volunteer_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, sa.ForeignKey("users.telegram_id"))
    volunteer = relationship("User", foreign_keys=[volunteer_id])
    request_status: Mapped[EvacuationRequestStatus]
    request_date: Mapped[datetime]
    evacuation_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f'< Evacuation Request: {self.request_id}, User: {self.user_id} ' \
               f'Volunteer: {self.volunteer_id} Region: {self.region_id}>'


class EvacuationRequestView(ModelView):
    column_list = ('request_id', 'region_id', 'user_id', 'city', 'street', 'home_number',
                   'flat_number', 'contact_first_name', 'contact_last_name', 'contact_phone_number', 'evacuation_qnt',
                   'volunteer_id', 'request_status', 'any_special_needs', 'special_needs',
                   'request_date', 'evacuation_at')
    form_columns = ('request_id', 'region_id', 'user_id', 'city', 'street', 'home_number', 'evacuation_qnt',
                    'flat_number', 'contact_first_name', 'contact_last_name',
                    'contact_phone_number', 'volunteer_id', 'request_status', 'any_special_needs', 'special_needs',
                    'request_date', 'evacuation_at')
    column_searchable_list = ['request_id', 'region_id', 'user_id', 'city', 'street', 'home_number',
                              'flat_number', 'contact_first_name', 'contact_last_name',
                              'contact_phone_number', 'evacuation_qnt', 'volunteer_id', 'request_status']
    column_filters = ['request_status', 'request_date', 'evacuation_at', 'any_special_needs']
    page_size = ADMIN_PANEL_PAGE_SIZE
