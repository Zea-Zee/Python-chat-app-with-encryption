from datetime import datetime
from sqlalchemy import JSON, DateTime, MetaData, Table, Column, String, Integer, TIMESTAMP, Numeric

from database import metadata

operation = Table(
    'operation',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('instrument', String, nullable=False),
    Column('type', String, nullable=False),
    # Column('datetime', TIMESTAMP, nullable=False),
    Column('datetime', DateTime(timezone=False), nullable=False),
    Column('quantity', Numeric(20, 8), nullable=False),
    # Column('quantity', String, nullable=False),
    Column('pair', String, nullable=False)
)
