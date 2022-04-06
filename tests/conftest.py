from . import fixture
from . import patch
from . import mock_manager
from . import ExternalLegalLogicMocks
from . import ExternalUserLogicMocks


def start_app():
    print("\n", "*" * 100, "\n")
    print("Tests Started")
    yield

    print("\n", "*" * 100, "\n")
    print("Tests Finished")


@fixture(autouse=True)
def mocks():
    mock_manager.reset()

    mock_manager.add_creator(ExternalLegalLogicMocks)
    mock_manager.add_creator(ExternalUserLogicMocks)

    mock_manager.build()
