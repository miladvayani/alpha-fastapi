from . import fixture
from . import mock_manager
from . import DataLayerLogicMocks


def setup_app():
    # print("\n", "*" * 100, "\n")
    print("Tests Started")
    yield

    # print("\n", "*" * 100, "\n")
    print("Tests Finished")


@fixture(autouse=True)
def mocks():
    mock_manager.reset()

    mock_manager.add_creator(DataLayerLogicMocks)

    mock_manager.build()
