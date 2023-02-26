
import sqlalchemy

import yaml

import jmon.database
import jmon.config
from jmon.errors import EnvironmentCreateError, EnvironmentHasRegisteredChecksError
import jmon.models
import jmon.run
from jmon.logger import logger


class Environment(jmon.database.Base):

    @classmethod
    def get_all(cls):
        """Get all checks"""
        session = jmon.database.Database.get_session()
        return session.query(cls).all()

    @classmethod
    def get_by_name(cls, name):
        """Get all checks"""
        session = jmon.database.Database.get_session()
        return session.query(cls).filter(cls.name==name).first()

    @classmethod
    def create(cls, name):
        """Create environment"""
        session = jmon.database.Database.get_session()
        pre_existing_environment = cls.get_by_name(name=name)
        if pre_existing_environment:
            return EnvironmentCreateError("An environment already exists with this name")

        instance = cls(name=name)
        session.add(instance)
        session.commit()
        return instance

    def delete(self):
        """Delete environment"""
        checks = [
            check
            for check in jmon.models.check.Check.get_by_environment(self)
        ]
        if checks:
            raise EnvironmentHasRegisteredChecksError(
                "Checks are registered against the environment")
        session = jmon.database.Database.get_session()
        session.delete(self)
        session.commit()

    __tablename__ = 'environment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(jmon.database.Database.GeneralString, unique=True, nullable=False)
