
import os

class Config:

    _INSTANCE = None

    DATABASE_TYPE = os.environ.get("DB_TYPE")
    DATABASE_HOST = os.environ.get("DB_HOST")
    DATABASE_PORT = os.environ.get("DB_PORT")
    DATABASE_USERNAME = os.environ.get("DB_USERNAME")
    DATABASE_PASSWORD = os.environ.get("DB_PASSWORD")
    DATABASE_NAME = os.environ.get("DB_NAME")

    DEFAULT_CHECK_INTERVAL = float(os.environ.get('DEFAULT_CHECK_INTERVAL', '0.5'))

    @property
    def DATABASE_URL(self):
        """Return database url"""
        sqlalchemy_type = None
        if self.DATABASE_TYPE == "postgresql":
            sqlalchemy_type = "postgresql+psycopg2"

        if sqlalchemy_type is None:
            raise Exception("Unrecognised DB_TYPE")

        return f"{sqlalchemy_type}://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    @classmethod
    def get(cls):
        """Get instance of config"""
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE
