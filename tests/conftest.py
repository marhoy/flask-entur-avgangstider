import pytest
import rutertider


@pytest.fixture
def app():
    app = rutertider.app
    return app
