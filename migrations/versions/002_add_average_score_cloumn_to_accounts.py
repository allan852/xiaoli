from sqlalchemy import *
from migrate import *
from xiaoli.models.account import Account

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    Account.metadata.bind = migrate_engine
    score_average = Column('average_score', Integer(2), default=0)
    create_column(score_average, Accoount.__table__)

    score_count = Column('score_count', Integer(11), default=0)
    create_column(score_count, Accoount.__table__)

    score_total = Column('score_total', Integer(11), default=0)
    create_column(score_total, Accoount.__table__)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    Account.metadata.bind = migrate_engine
    drop_column("score_average", Account.__table__)
    drop_column("score_count", Account.__table__)
    drop_column("score_total", Account.__table__)
