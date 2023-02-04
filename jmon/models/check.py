

import sqlalchemy

import jmon.database


class Check(jmon.database.Base):

    __tablename__ = 'check'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    config = sqlalchemy.Column(jmon.database.Database.LargeString)
