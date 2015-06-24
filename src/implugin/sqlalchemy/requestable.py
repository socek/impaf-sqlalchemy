from sqlalchemy.orm import sessionmaker

from impaf.requestable import Requestable
from impaf.requestable import ImpafRequest
from impaf.utils import cached

from .driver import DriverHolder


class SqlalchemyRequestable(Requestable):

    def feed_request(self, request):
        super().feed_request(request)
        self.generate_drivers()

    @property
    def database(self):
        return self.request.database

    def generate_drivers(self):
        self.drivers = self._get_driver_holder_cls()(self.database)
        self.drivers.generate_drivers()

    def _get_request_cls(self):
        return SqlalchemyRequest

    def _get_driver_holder_cls(self):
        return DriverHolder


class DatabaseConnection(object):

    def init(self, settings, registry):
        self.settings = settings
        self.registry = registry
        self._cache = {}

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


class SqlalchemyRequest(ImpafRequest, DatabaseConnection):
    pass
