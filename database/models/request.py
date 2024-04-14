from typing import Optional

import sqlalchemy as sa

from flask import flash
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from database.base import Base
from database.connector import session
from database.models.region import Region
from bot.utils.enums import RequestStatus, RequestType
from background_tasks import accept_request, rate_request

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
    column_list = ('region_id', 'city', 'street', 'home_number',
                   'flat_number', 'contact_first_name', 'contact_last_name', 'contact_phone_number', 'request_text',
                   'type', 'request_status', 'request_date')
    column_searchable_list = ['region_id', 'city', 'street', 'home_number',
                              'flat_number', 'contact_first_name', 'contact_last_name',
                              'contact_phone_number', 'request_text', 'request_status']
    column_filters = ['request_status', 'request_date', 'region']
    page_size = ADMIN_PANEL_PAGE_SIZE
    can_edit = False
    can_create = False
    can_delete = False
    can_export = False
    can_view_details = True

    def _format_region(view, context, model, name):
        with session() as s:
            region = s.query(Region).filter(Region.region_id==model.region_id).first()
        return region.region_name

    def _enum_type_to_str(view, context, model, name):
        return model.type.value

    column_formatters = {
        'region_id': _format_region,
        'type': _enum_type_to_str,
    }

    @action('take_in_progress', 'Взяти в роботу', 'Ви впевнені, що ви готові взяті ці запити на волонтерську допомогу?')
    def take_in_progress(self, ids):
        # Get query for the selected items
        success_update = 0
        for request_id in ids:
            request_id = int(request_id)
            with session() as s:
                request = s.query(Request).filter(Request.request_id == request_id).first()
                if request.volunteer_id is None and request.request_status == RequestStatus.created:
                    success_update += 1
                    request.volunteer_id = 388309639
                    request.request_status = RequestStatus.taken_by_volunteer
                    s.add(request)
                    s.commit()
                    accept_request.delay(request.volunteer_id, request.user_id)

        # Optional: provide feedback to the user
        flash(f"Успішно оновлено {success_update} запитів", 'success')

    @action('finish_request', 'Запити виконані', 'Ви впевнені, цю дію не можливо відмінити?')
    def finish_request(self, ids):
        # Get query for the selected items
        success_update = 0
        for request_id in ids:
            request_id = int(request_id)
            with session() as s:
                request = s.query(Request).filter(Request.request_id == request_id).first()
                if request.volunteer_id is not None and request.request_status == RequestStatus.taken_by_volunteer:
                    success_update += 1
                    request.volunteer_id = 388309639
                    request.request_status = RequestStatus.delivered
                    s.add(request)
                    s.commit()
                    rate_request.delay(request.volunteer_id, request.user_id, request_id)

        # Optional: provide feedback to the user
        flash(f"Успішно оновлено {success_update} запитів", 'success')
