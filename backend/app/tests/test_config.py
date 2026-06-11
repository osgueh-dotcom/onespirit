import pytest

from app.core.config import Settings


def production_settings(**overrides):
    values = {
        "ENV": "production",
        "DEBUG": False,
        "SEED_DEMO_USER": False,
        "SEED_PLACEHOLDER_USERS": False,
        "DB_PASSWORD": "production-db-password",
        "JWT_SECRET": "production-jwt-secret-with-sufficient-length",
        "ADMIN_PASSWORD": "ProductionAdmin1!",
        "DEMO_PASSWORD": "ProductionDemo1!",
        "BACKEND_CORS_ORIGINS": ["https://workflow.example.com"],
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_production_settings_reject_debug_mode():
    with pytest.raises(ValueError, match="DEBUG must be disabled"):
        production_settings(DEBUG=True)


def test_production_settings_reject_default_database_password():
    with pytest.raises(ValueError, match="DB_PASSWORD must be changed"):
        production_settings(DB_PASSWORD="onespirit_pass")


@pytest.mark.parametrize("setting_name", ["SEED_DEMO_USER", "SEED_PLACEHOLDER_USERS"])
def test_production_settings_reject_demo_seed_flags(setting_name):
    with pytest.raises(ValueError, match=f"{setting_name} must be disabled"):
        production_settings(**{setting_name: True})


def test_production_settings_accept_rotated_values():
    configured = production_settings()

    assert configured.ENV == "production"
    assert configured.DEBUG is False
