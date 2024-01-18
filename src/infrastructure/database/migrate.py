import os
from alembic.config import Config
import alembic.command as alembic_command


def migrate_db():
    config = Config(f"{os.path.dirname(__file__)}/alembic.ini")
    alembic_command.upgrade(config, 'head')


if __name__ == '__main__':
    migrate_db()
