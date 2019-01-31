from importlib import import_module
from pathlib import PurePath
from typing import Tuple, Union, Sequence, Type, List

import connexion
import yaml
from connexion import FlaskApp, RestyResolver
from flask import Flask, Blueprint

from sakura_village.extensions import ADMIN, DB, MIGRATE

base_dir = PurePath(__file__).parent
specification_dir = PurePath(__file__).parent.joinpath('specification')
config_path = base_dir.joinpath('config.yml')


def discover_models() -> Sequence[Type[DB.Model]]:
    # todo: 使用 pkgutil.walk_packages 递归发现模型类
    ret = []

    mod = import_module('sakura_village.models')
    for name in dir(mod):
        attr = getattr(mod, name, None)
        if isinstance(attr, type) and issubclass(getattr(mod, name, None), DB.Model):
            ret.append(mod)

    return ret


def discover_blueprint() -> Sequence[Tuple[Blueprint, Union[str, None]]]:
    # todo: 通过 pkgutil.walk_packages 发现 blueprints
    ret: List[Tuple[Blueprint, Union[str, None]]] = []

    # mod = import_module('sakura_village.view')
    # if getattr(mod, 'BP', None) is not None:
    #     ret.append((getattr(mod, 'BP'), getattr(mod, 'PREFIX', None)))

    return ret


def create_app() -> connexion.FlaskApp:
    # create connexion app
    con_app: FlaskApp = connexion.App(__name__)
    # con_app.server = 'gevent'
    con_app.specification_dir = specification_dir
    con_app.resolver = RestyResolver('sakura_village.api')

    # setup OpenAPI specification
    con_app.add_api(specification_dir.joinpath('openapi.yml'), base_path="/api")

    # setup flask app
    flask_app: Flask = con_app.app
    flask_app.config.from_mapping(yaml.load(open(config_path, encoding='utf-8')))

    # setup flask extensions
    ADMIN.init_app(flask_app)
    DB.init_app(flask_app)
    MIGRATE.init_app(flask_app, DB)

    # discover models
    discover_models()

    # setup extra flask blueprints
    for bp, prefix in discover_blueprint():
        flask_app.register_blueprint(BP, url_prefix=prefix)

    #
    # factory end here
    # ========================================================================
    return con_app


connexion_app: FlaskApp = create_app()
app: Flask = connexion_app.app

if __name__ == "__main__":
    connexion_app.run(port=5000)
