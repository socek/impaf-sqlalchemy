from mock import MagicMock

from pytest import fixture

from impaf.testing import RequestFixture, ControllerFixture


class SqlalchemyRequestFixture(RequestFixture):

    @fixture
    def mdatabase(self, request):
        return MagicMock()


class SqlalchemyControllerFixture(
    SqlalchemyRequestFixture,
    ControllerFixture,
):

    @fixture
    def controller(self, root_factory, mrequest, context, mdrivers):
        controller = super().controller(root_factory, mrequest, context)
        controller.drivers = mdrivers
        return controller

    @fixture
    def mdrivers(self):
        return MagicMock()
