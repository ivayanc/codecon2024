from typing import Optional

import sqlalchemy as sa

from flask import flash
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from database.base import Base
from database.models.region import Region
from database.models.user import User
from database.connector import session
from bot.utils.enums import EvacuationRequestStatus
from background_tasks import accept_evacuation_request, rate_evacuation_request

from configuration import ADMIN_PANEL_PAGE_SIZE


class EvacuationRequest(Base):
    __tablename__ = 'evacuation_request'
    request_id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True)
    region = relationship("Region", backref="evacuation_requests")
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
    column_list = ('region_id', 'city', 'street', 'home_number',
                   'flat_number', 'contact_first_name', 'contact_last_name', 'contact_phone_number', 'evacuation_qnt',
                   'request_status', 'any_special_needs', 'special_needs', 'request_date')
    form_columns = ('region_id', 'city', 'street', 'home_number', 'evacuation_qnt',
                    'flat_number', 'contact_first_name', 'contact_last_name',
                    'contact_phone_number', 'request_status', 'any_special_needs', 'special_needs', 'request_date')
    column_searchable_list = ['region_id', 'city', 'street', 'home_number', 'flat_number',
                              'contact_first_name', 'contact_last_name',
                              'contact_phone_number', 'evacuation_qnt', 'request_status']
    column_filters = ['region', 'request_status', 'request_date', 'any_special_needs', 'region']
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

    column_formatters = {
        'region_id': _format_region,
    }

    @action('take_in_progress', 'Взяти в роботу', 'Ви впевнені, що ви готові взяті ці запити на евакуацію?')
    def take_in_progress(self, ids):
        # Get query for the selected items
        success_update = 0
        for request_id in ids:
            request_id = int(request_id)
            with session() as s:
                request = s.query(EvacuationRequest).filter(EvacuationRequest.request_id == request_id).first()
                if request.volunteer_id is None and request.request_status == EvacuationRequestStatus.created:
                    success_update += 1
                    request.volunteer_id = 388309639
                    request.request_status = EvacuationRequestStatus.taken_by_volunteer
                    s.add(request)
                    s.commit()
                    accept_evacuation_request.delay(request.volunteer_id, request.user_id)

        # Optional: provide feedback to the user
        flash(f"Успішно оновлено {success_update} запитів", 'success')

    @action('finish_request', 'Запити виконані', 'Ви впевнені, цю дію не можливо відмінити?')
    def finish_request(self, ids):
        # Get query for the selected items
        success_update = 0
        for request_id in ids:
            request_id = int(request_id)
            with session() as s:
                request = s.query(EvacuationRequest).filter(EvacuationRequest.request_id == request_id).first()
                if request.volunteer_id is not None and request.request_status == EvacuationRequestStatus.taken_by_volunteer:
                    success_update += 1
                    request.volunteer_id = 388309639
                    request.request_status = EvacuationRequestStatus.evacuation_ended
                    s.add(request)
                    s.commit()
                    rate_evacuation_request.delay(request.volunteer_id, request.user_id, request_id)

        # Optional: provide feedback to the user
        flash(f"Успішно оновлено {success_update} запитів", 'success')

