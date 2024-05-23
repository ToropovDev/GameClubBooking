from sqlalchemy import MetaData, Integer, Table, Column

metadata = MetaData()

pc_station = Table(
    'pc_station',
           metadata,
           Column('id', Integer, primary_key=True),
           )


