import os
from dataclasses import dataclass
import dotenv


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    token: str


@dataclass
class BotConfig:
    bot: TgBot
    db: DatabaseConfig


def load_config():
    dotenv.load_dotenv()
    return BotConfig(bot=TgBot(token=os.getenv('TOKEN')),
                     db=DatabaseConfig('a', 'a', 'a', 'a'))
