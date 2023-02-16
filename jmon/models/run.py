

import sqlalchemy
import sqlalchemy.orm

import jmon.database
import jmon.config


class Run(jmon.database.Base):

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
    def create(cls, check):
        """Create run"""
        session = jmon.database.Database.get_session()
        run = cls(check=check)

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

    timestamp = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.sql.func.now(), primary_key=True)
    success = sqlalchemy.Column(sqlalchemy.Boolean)

    @property
    def timestamp_key(self):
        """Return key value for timestamp"""
        return self.timestamp.strftime('%Y-%m-%d_%H-%M-%S') if self.timestamp else None

    def set_success(self, success):
        """Set success value"""
        session = jmon.database.Database.get_session()
        self.success = success
        session.add(self)
        session.commit()
