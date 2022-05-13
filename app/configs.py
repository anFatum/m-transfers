import os
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), verbose=True)
DEFAULT_CONFIG = None


class Configs:
    DEBUG = False
    ENVIRONMENT = "production"

    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    USE_HTTPS = os.getenv("USE_HTTPS", "False").lower() in ["true", "1"]
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    AUTH_TYPE = os.getenv("AUTH_PROVIDER", "local")
    # region Database
    DB_DRIVER = os.getenv("driver", "sqlite")
    DB_USERNAME = os.getenv("username")
    DB_PASSWORD = os.getenv("password")
    DB_HOST = os.getenv("host")
    DB_PORT = os.getenv("port")
    DB_DATABASE = os.getenv("database")
    DB_CONNECTION_STRING = None
    # endregion Database


class DevelopmentConfigs(Configs):
    DEBUG = True
    ENVIRONMENT = "development"
    DB_CONNECTION_STRING = "sqlite:////database.db"


class TestingConfigs(Configs):
    DEBUG = True
    ENVIRONMENT = "testing"
    DB_CONNECTION_STRING = "sqlite:////test_database.db"


class ProductionConfigs(Configs):
    DEBUG = False
    ENVIRONMENT = "production"


_CONFIG_DICT = {
    "dev": DevelopmentConfigs,
    "prod": ProductionConfigs,
    "test": TestingConfigs
}


def get_config(config: str = "dev"):
    try:
        global DEFAULT_CONFIG
        DEFAULT_CONFIG = DEFAULT_CONFIG if DEFAULT_CONFIG is not None \
            else _CONFIG_DICT[config]
        if not DEFAULT_CONFIG.DB_CONNECTION_STRING:
            DEFAULT_CONFIG.DB_CONNECTION_STRING = _construct_connection_string(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    except KeyError:
        raise KeyError("No environment configs found")


def _construct_connection_string(cfg: Configs):
    """
    Function to build connection string.
    :return: built connection string to database
    """
    connection_string = os.getenv("DB_CONNECTION_STRING")
    if connection_string:
        return connection_string

    driver_prefix = f"{cfg.DB_DRIVER}://"
    if cfg.DB_DRIVER.lower() == 'sqlite':
        driver_prefix += "//" if sys.platform == "win32" else "/"

    auth = None
    if cfg.DB_USERNAME:
        auth = cfg.DB_USERNAME
    if cfg.DB_PASSWORD:
        auth = f"{auth}:{cfg.DB_PASSWORD}"
    auth = f"{auth}@" if auth else ""

    return f"{driver_prefix}{auth}{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_DATABASE}"
