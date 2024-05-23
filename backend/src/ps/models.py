from sqlalchemy import MetaData, Integer, Table, Column

metadata = MetaData()

ps_station = Table(
    'ps_station',
           metadata,
           Column('id', Integer, primary_key=True),
           )

