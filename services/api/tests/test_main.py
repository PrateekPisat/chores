from chores_client.main import create_app


class _Config:
    def __init__(self, environment: str | None):
        self.environment = environment


def test_debug_is_off_in_production(monkeypatch):
    monkeypatch.setattr("chores_client.main.load_config", lambda: _Config("production"))

    app = create_app([])

    assert app.debug is False


def test_debug_stays_on_outside_production(monkeypatch):
    monkeypatch.setattr("chores_client.main.load_config", lambda: _Config("local"))

    app = create_app([])

    assert app.debug is True
