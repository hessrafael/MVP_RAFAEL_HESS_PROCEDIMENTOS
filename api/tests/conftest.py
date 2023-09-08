import os
os.environ["CONFIG"] = "TEST"
import pytest
import app

class SalaValue1:
    id = None

class SalaValue2:
    id = None

class ProcValue1:
    id = None

class ProcValue2:
    id = None

@pytest.fixture(scope='module')
def test_client():
    app.app.config.update({
        "TESTING": True,
    })    
    with app.app.test_client() as testing_client:
        with app.app.app_context():
            yield testing_client

