import os
from alembic.config import Config
import alembic.command as alembic_command


def make_migration():
    config = Config(f"{os.path.dirname(__file__)}/alembic.ini")
    alembic_command.revision(config, autogenerate=True)


if __name__ == '__main__':
    make_migration()
