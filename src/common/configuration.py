from os import getenv
from dataclasses import dataclass

from sqlalchemy.engine import URL
from dotenv import load_dotenv
load_dotenv()


@dataclass
class BaseConfig:
    domain: str | None = getenv("DOMAIN_NAME")

    def __post_init__(self):
        required_vars = [
            "domain",
        ]
        for var in required_vars:
            value = getattr(self, var)
            if value is None:
                raise ValueError(f"Environment variable for {var} is not set")


@dataclass
class DatabaseConfig:
    host: str = getenv("DB_HOST", "db")
    port: int = int(getenv("DB_PORT", 5432))
    user: str | None = getenv("DB_USER")
    password: str | None = getenv("DB_PASS", None)
    name: str | None = getenv("DB_NAME")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def __post_init__(self):
        required_vars = ["name", "user", "password", "port", "host"]
        for var in required_vars:
            value = getattr(self, var)
            if value is None:
                raise ValueError(f"Environment variable for {var} is not set")

    def build_connection_str(self, test_db: bool = False) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port if not test_db else 5433,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    """Redis connection variables."""

    db: int = int(getenv("REDIS_DATABASE", 1))
    """ Redis Database ID """
    host: str = getenv("REDIS_HOST", "redis")
    port: int = int(getenv("REDIS_PORT", 6379))
    passwd: str | None = getenv("REDIS_PASSWORD")
    username: str | None = getenv("REDIS_USERNAME")
    state_ttl: str | None = getenv("REDIS_TTL_STATE", None)
    data_ttl: str | None = getenv("REDIS_TTL_DATA", None)

    def __post_init__(self):
        required_vars = ["db", "host", "passwd"]
        for var in required_vars:
            value = getattr(self, var)
            if value is None:
                raise ValueError(f"Environment variable for {var} is not set")


@dataclass
class TokenConfig:
    default_encoding: str = "utf-8"
    jwt_sign_algorithm: str = "HS256"
    secret_key: str | None = getenv("TOKEN_SECRET_KEY")
    access_token_expire_minutes: int = 12 * 60

    def __post_init__(self):
        required_vars = ["secret_key"]
        for var in required_vars:
            value = getattr(self, var)
            if value is None:
                raise ValueError(f"Environment variable for {var} is not set")


@dataclass
class SmtpConfig:
    username: str | None = getenv("SMTP_USERNAME")
    password: str | None = getenv("SMTP_PASSWORD")
    server: str | None = getenv("SMTP_SERVER")
    port: int | None = int(getenv("SMTP_PORT", 587))

    def __post_init__(self):
        required_vars = ["username", "password", "server", "port"]
        for var in required_vars:
            value = getattr(self, var)
            if value is None:
                raise ValueError(f"Environment variable for {var} is not set")


@dataclass
class Configuration:
    debug = bool(getenv("DEBUG", False))
    base = BaseConfig()
    db = DatabaseConfig()
    redis = RedisConfig()
    token = TokenConfig()
    smtp = SmtpConfig()


conf = Configuration()
