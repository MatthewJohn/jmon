

import sqlalchemy

import yaml
import json

import jmon.database


class Check(jmon.database.Base):

    @classmethod
    def from_yaml(cls, yml):
        """Return instance of class from check yaml"""
        try:
            content = yaml.safe_load(yml)
        except Exception as exc:
            raise Exception('Invalid YAML')

        if type(content) is not dict:
            raise Exception("YAML must be a dictionary")

        if not (name := content.get("name")):
            raise Exception("No name defined for check")

        if not (steps := content.get("steps")):
            raise Exception("No steps defined for check")

        # Check for existing steps with the same name
        session = jmon.database.Database.get_session()
        instance = session.query(cls).filter(cls.name==name).first()
        # Create new instance of check, if it doesn't exist
        if not instance:
            instance = cls(name=name)

        instance.steps = steps

        session.add(instance)
        session.commit()

        return instance


    __tablename__ = 'check'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(jmon.database.Database.GeneralString, primary_key=True)
    _steps = sqlalchemy.Column(jmon.database.Database.LargeString, name="config")

    @property
    def steps(self):
        """Return steps dictionary"""
        return json.loads(self._steps)

    @steps.setter
    def steps(self, value):
        """Set steps in database"""
        self._steps = json.dumps(value)