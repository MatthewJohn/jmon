

import datetime
import sqlalchemy
import sqlalchemy.orm

import jmon.database
import jmon.config


class Run(jmon.database.Base):

    TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'

    @classmethod
    def get_latest_by_check(cls, check):
        """Get latest check by run"""
        session = jmon.database.Database.get_session()
        return session.query(cls).filter(cls.check==check).order_by(cls.timestamp.desc).limit(1).first()

    @classmethod
    def get_by_check(cls, check):
        """Get all runs by check"""
        session = jmon.database.Database.get_session()
        return [run for run in session.query(cls).filter(cls.check==check)]

    @classmethod
    def get(cls, check, timestamp_id):
        """Return run for check and timestamp"""
        session = jmon.database.Database.get_session()
        return session.query(cls).filter(cls.check==check, cls.timestamp_id==timestamp_id).first()

    @classmethod
    def create(cls, check):
        """Create run"""
        session = jmon.database.Database.get_session()
        run = cls(check=check)
        timestamp = datetime.datetime.now()
        run.timestamp = timestamp
        run.timestamp_id = timestamp.strftime(cls.TIMESTAMP_FORMAT)

        session.add(run)
        session.commit()

        return run

    __tablename__ = 'run'

    check_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("check.id", name="fk_run_check_id_check_id"),
        nullable=False,
        primary_key=True
    )
    check = sqlalchemy.orm.relationship("Check", foreign_keys=[check_id])

    # String representation of the tiemstamp, in the format of
    # the tiemstamp_key
    timestamp_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    # Datetime timestamp of check
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime)

    success = sqlalchemy.Column(sqlalchemy.Boolean)

    def set_success(self, success):
        """Set success value"""
        session = jmon.database.Database.get_session()
        self.success = success
        session.add(self)
        session.commit()
