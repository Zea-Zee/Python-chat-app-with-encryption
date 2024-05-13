from datetime import datetime
from sqlalchemy import JSON, MetaData, Table, Column, String, Integer, TIMESTAMP, Numeric


metadata = MetaData()

operation = Table(
    'operation',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('instrument', String, nullable=False),
    Column('type', String, nullable=False),
    Column('datetime', TIMESTAMP, nullable=False),
    Column('quantity', Numeric(20, 8), nullable=False),
    Column('pair', String, nullable=False)
)
