from sqlalchemy import MetaData, Integer, Table, Column

metadata = MetaData()

vr_station = Table(
    'vr_station',
           metadata,
           Column('id', Integer, primary_key=True),
           )

