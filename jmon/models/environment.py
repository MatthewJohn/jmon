
import sqlalchemy

import yaml

import jmon.database
import jmon.config
from jmon.errors import EnvironmentCreateError
import jmon.models.run
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
    def from_yaml(cls, yml):
        """Return instance of class from check yaml"""
        try:
            content = yaml.safe_load(yml)
        except Exception as exc:
            raise EnvironmentCreateError('Invalid YAML')

        if type(content) is not dict:
            raise EnvironmentCreateError("YAML must be a dictionary")

        if not (name := content.get("name")):
            raise EnvironmentCreateError("No name defined for environment")

        # Check for existing steps with the same name
        session = jmon.database.Database.get_session()

        instance = session.query(cls).filter(cls.name==name).first()
        # Create new instance of environment, if it doesn't exist
        if not instance:
            instance = cls(name=name)

        session.add(instance)
        session.commit()

        return instance


    __tablename__ = 'environment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(jmon.database.Database.GeneralString, unique=True, nullable=False)
