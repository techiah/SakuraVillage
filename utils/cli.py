from importlib import import_module

import click
from flask.cli import AppGroup

from utils.sqla import list_models

try:
    from flask_sqlalchemy import SQLAlchemy
except ImportError:
    # Dummy class for type annotation
    class SQLAlchemy:
        ...

from utils.imp import import_recursive


def cli_discover(db: SQLAlchemy):
    discover_group = AppGroup('discover')

    @discover_group.command()
    @click.argument('path')
    def models(path):
        pkg = import_module(path)
        import_recursive(pkg)
        for model in list_models(db):
            print(model)

    return discover_group
