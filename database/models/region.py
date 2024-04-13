from typing import Optional

import sqlalchemy as sa

from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from database.base import Base

from configuration import ADMIN_PANEL_PAGE_SIZE


class Region(Base):
    __tablename__ = 'region'
    region_id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True)
    region_name: Mapped[str]

    def __repr__(self):
        return f'< Code: {self.region_id}, Name: {self.region_name} >'


class RegionView(ModelView):
    column_list = ('region_id', 'region_name')
    form_columns = ('region_id', 'region_name')
    column_searchable_list = ['region_id', 'region_name']
    page_size = ADMIN_PANEL_PAGE_SIZE
