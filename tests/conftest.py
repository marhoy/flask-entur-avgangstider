import pytest
import rutertider


@pytest.fixture
def app():
    app = rutertider.create_app()
    return app
