from sqlalchemy.orm import sessionmaker

from impaf.requestable import Requestable
from impaf.requestable import ImpafRequest
from impaf.utils import cached


class SqlalchemyRequestable(Requestable):

    def _get_request_cls(self):
        return SqlalchemyRequest

    @property
    def database(self):
        return self.request.database


class SqlalchemyRequest(ImpafRequest):

    @cached
    def database(self):
        if self.settings['db']['type'] == 'sqlite':
            return self._get_sqlite_database()
        else:
            return self._get_normal_database()

    def _get_sqlite_database(self):
        engine = self.registry['db_engine']
        return sessionmaker(bind=engine)()

    def _get_normal_database(self):
        db = self.registry['db']
        db.expire_all()
        return db
