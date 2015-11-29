from mock import MagicMock

from pytest import fixture

from impaf.testing import RequestCase
from impaf.testing import ControllerFixture
from impaf.testing import RequestFixture
from impaf.testing import cache


class SqlalchemyRequestFixture(RequestFixture):

    @fixture
    def mdatabase(self, mrequest):
        mrequest.database = MagicMock()
        return mrequest.database

    @fixture
    def mdrivers(self, testable):
        testable.drivers = MagicMock()
        return testable.drivers


class SqlalchemyControllerFixture(
    SqlalchemyRequestFixture,
    ControllerFixture,
):
    pass


class DriverFixture(object):

    @fixture
    def mdatabase(self):
        return MagicMock()

    @fixture
    def query(self, mdatabase):
        return mdatabase().query

    @fixture
    def driver(self, mdatabase):
        driver = self._cls_driver()()
        driver.feed_database(mdatabase)
        return driver


class SqlalchemyCase(RequestCase):

    @cache
    def mdatabase(self):
        return self.pobject(self.object(), 'database')

    @cache
    def mdrivers(self):
        return self.pobject(self.object(), 'drivers')
