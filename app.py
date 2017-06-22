# coding=utf-8
"""
主应用
"""
from flask import Flask, Markup, render_template, request

# We import the markdown library
import markdown
# from lib.yundama import YDMHttp
from pyblog.peewee_storage import resetdb
from telesoho.utils import JSON
from werkzeug.contrib.cache import SimpleCache

THE_APP = Flask(__name__, static_url_path='')

@THE_APP.route("/")
def index():
    """
    Index file
    """

    content = """
Chapter
=======

Section
-------

* Item 1
* Item 2

```sh
sh batch.
```
"""

    content = Markup(markdown.markdown(content))
    return render_template('index.html', **locals())


@THE_APP.route("/yundama", methods=['POST'])
def yundama():
    """
    云打码接口
    """
    obj = request.get_json(True)
    return JSON.dumps(obj)

@THE_APP.route("/addpost", methods=['POST'])
def addpost():
    """
    新增文章
    """
    obj = request.get_json(True)
    return JSON.dumps(obj)

@THE_APP.cli.command()
def initdb():
    """Initialize the database."""
    __load_config()
    resetdb()

def __load_config():
    """
    Load all config file.
    """
    THE_APP.config.from_object("default_settings")

    THE_APP.config.from_envvar('PYBLOG_ENV', True)
    # 替换配置文件中的WorkspaceRoot变量
    THE_APP.config["DATABASE"] = THE_APP.config[
        "DATABASE"].format(WorkspaceRoot=THE_APP.root_path)
    THE_APP.logger.info(THE_APP.config['DATABASE'])

if __name__ == "__main__":
    __load_config()
    cache = SimpleCache()
    THE_APP.run(host='::')
