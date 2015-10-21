from sqlalchemy import *
from migrate import *
from xiaoli.models.plan import PlanKeyword

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    PlanKeyword.metadata.bind = migrate_engine
    type = Column('type', String(64), default=PlanKeyword.TYPE_USERADD)
    create_column(type, PlanKeyword.__table__)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    PlanKeyword.metadata.bind = migrate_engine
    drop_column("type", PlanKeyword.__table__)
