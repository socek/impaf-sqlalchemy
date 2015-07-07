from mock import MagicMock
from mock import patch

from pytest import fixture
from pytest import yield_fixture

from impaf.testing import RequestFixture

from ..driver import DriverHolder
from ..requestable import DatabaseConnection
from ..requestable import SqlalchemyRequest
from ..requestable import SqlalchemyRequestable


class TestSqlalchemyRequestable(RequestFixture):

    @fixture
    def requestable(self, request):
        return SqlalchemyRequestable()

    def test_get_request_cls(self, requestable):
        requestable._get_request_cls() is SqlalchemyRequest

    def test_get_driver_holder_cls(self, requestable):
        requestable._get_driver_holder_cls() is DriverHolder


class TestDatabaseConnection(RequestFixture):

    @fixture
    def obj(self, settings, registry):
        settings['db'] = {}
        connection = DatabaseConnection()
        connection.init(settings, registry)
        return connection

    @yield_fixture
    def msessionmaker(self):
        patcher = patch('implugin.sqlalchemy.requestable.sessionmaker')
        with patcher as mock:
            yield mock

    def test_postgresql(self, obj, settings, registry):
        settings['db']['type'] = 'postgresql'
        registry['db'] = MagicMock()

        assert obj.database() == registry['db']
        registry['db'].expire_all.assert_called_once_with()

    def test_sqlite(self, obj, settings, registry, msessionmaker):
        settings['db']['type'] = 'sqlite'
        engine = MagicMock()
        registry['db_engine'] = engine

        assert obj.database() == msessionmaker.return_value.return_value
        msessionmaker.assert_called_once_with(bind=engine)