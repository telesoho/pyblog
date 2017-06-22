# -*- coding:utf-8 -*-
"""
main.py
"""
import os
import sys
from empty import Empty


# apps is a special folder where you can place your blueprints
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))

BASESTRING = getattr(__builtins__, 'basestring', str)


class App(Empty):
    pass


def config_str_to_obj(cfg):
    """
    load config object
    """
    if isinstance(cfg, BASESTRING):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg


def app_factory(config, app_name, blueprints=None):
    """
    App factory
    """
    # you can use Empty directly if you wish
    app = App(app_name)
    config = config_str_to_obj(config)

    app.configure(config)
    app.add_blueprint_list(blueprints or config.BLUEPRINTS)
    app.setup()

    return app


def wsgi():
    """
    An empty app
    """
    from config import common
    # setup app through APP_CONFIG envvar
    return app_factory(common, common.PROJECT_NAME)


if __name__ == '__main__':
    wsgi()
