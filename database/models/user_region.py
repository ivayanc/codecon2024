from typing import Optional

import sqlalchemy as sa

from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from database.base import Base

from configuration import ADMIN_PANEL_PAGE_SIZE


class UserRegion(Base):
    __tablename__ = 'user_region'
    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True)
    region = relationship("Region")
    region_id: Mapped[int] = mapped_column(sa.ForeignKey("region.region_id"))
    user = relationship("User")
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.telegram_id"))
    volunteer_region: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'< Region: {self.region_id}, User: {self.user_id} Volunteering_region: {self.volunteer_region}>'


class UserRegionView(ModelView):
    column_list = ('region_id', 'user_id', 'volunteer_region')
    form_columns = ('region_id', 'user_id', 'volunteer_region')
    column_searchable_list = ['region_id', 'user_id']
    column_filters = ['volunteer_region']
    page_size = ADMIN_PANEL_PAGE_SIZE
