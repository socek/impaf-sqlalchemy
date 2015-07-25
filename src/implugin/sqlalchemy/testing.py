from mock import MagicMock

from pytest import fixture

from impaf.testing import RequestFixture, ControllerFixture


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
