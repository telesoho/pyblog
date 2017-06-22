# coding:utf-8

__all__ = ['Empty']

from flask import Flask, render_template
from werkzeug.utils import import_string
import logging


class NoExtensionException(Exception):
    pass


class BlueprintException(Exception):
    pass


BASESTRING = getattr(__builtins__, 'basestring', str)

# pylint: disable=W0612, W0613
class Empty(Flask):
    """
    An empty flask app.
    """

    def configure(self, config=None):
        """
        Load configuration class into flask app.

        If environment variable available, overwrites class config.
        """
        self.config.from_object(config)

        # could/should be available in server environment
        self.config.from_envvar("FLASK_CONFIG", silent=False)

    def add_blueprint(self, name, keyw):
        """
        Add blueprint
        """
        for module in self.config['LOAD_MODULES_EXTENSIONS']:
            try:
                __import__('%s.%s' % (name, module), fromlist=['*'])
            except ImportError as err:
                print(err)
            except AttributeError as err:
                print(err)

        blueprint = import_string('%s.%s' % (name, 'app'))
        self.register_blueprint(blueprint, **keyw)

    def add_blueprint_list(self, bp_list):
        """
        Add blueprint list
        """
        for blueprint_config in bp_list:
            name, keyw = None, dict()

            if isinstance(blueprint_config, BASESTRING):
                name = blueprint_config
                keyw.update({'url_prefix': '/' + name})
            elif isinstance(blueprint_config, (list, tuple)):
                name = blueprint_config[0]
                keyw.update(blueprint_config[1])
            else:
                raise BlueprintException(
                    "Error in BLUEPRINTS setup in config/common.py;"
                    "Please, verify if each blueprint setup is "
                    "either a string or a tuple."
                )

            self.add_blueprint(name, keyw)

    def setup(self):
        """
        Setup all
        """
        self.configure_logger()
        self.configure_error_handlers()
        self.configure_database()
        self.configure_context_processors()
        self.configure_template_extensions()
        self.configure_template_filters()
        self.configure_extensions()
        self.configure_before_request()
        self.configure_views()

    def configure_logger(self):
        """Configures the app logger."""
        log_filename = self.config['LOG_FILENAME']

        # Create a file logger since we got a logdir
        log_file = logging.FileHandler(filename=log_filename)
        formatter = logging.Formatter(self.config['LOG_FORMAT'])
        log_file.setFormatter(formatter)
        log_file.setLevel(self.config['LOG_LEVEL'])

        logger = self.logger
        logger.addHandler(log_file)
        logger.info("Logger started")


    def configure_error_handlers(self):
        """
        Configure all error handlers here
        """
        @self.errorhandler(403)
        def forbidden_page(error):
            """
            Shows a "access forbidden" page.

            The server understood the request, but is refusing to fulfill it.
            Authorization will not help and the request SHOULD NOT be repeated.
            If the request method was not HEAD and the server wishes to make
            public why the request has not been fulfilled, it SHOULD describe
            the reason for the refusal in the entity. If the server does not
            wish to make this information available to the client, the status
            code 404 (Not Found) can be used instead.
            """
            return render_template("http/access_forbidden.html"), 403

        @self.errorhandler(404)
        def page_not_found(error):
            """
            Shows a "not found" page.

            The server has not found anything matching the Request-URI. No
            indication is given of whether the condition is temporary or
            permanent. The 410 (Gone) status code SHOULD be used if the
            server knows, through some internally configurable mechanism,
            that an old resource is permanently unavailable and has no
            forwarding address. This status code is commonly used when the
            server does not wish to reveal exactly why the request has been
            refused, or when no other response is applicable.
            """
            return render_template("http/page_not_found.html"), 404

        @self.errorhandler(405)
        def method_not_allowed_page(error):
            """
            Shows a "method not allowed" page.

            The method specified in the Request-Line is not allowed for the
            resource identified by the Request-URI. The response MUST
            include an Allow header containing a list of valid methods
            for the requested resource.
            """
            return render_template("http/method_not_allowed.html"), 405

        @self.errorhandler(500)
        def server_error_page(error):
            """Shows a "server error" page."""
            return render_template("http/server_error.html"), 500

    def configure_database(self):
        """Database configuration should be set here."""
        pass

    def configure_context_processors(self):
        """Modify templates context here."""
        pass

    def configure_template_extensions(self):
        """Add jinja2 extensions here."""
        # 'do' extension.
        # see: http://jinja.pocoo.org/docs/extensions/#expression-statement
        self.jinja_env.add_extension('jinja2.ext.do')

    def configure_template_filters(self):
        """Configures filters and tags for jinja."""
        pass

    def configure_extensions(self):
        """Configures extensions like mail and login here."""
        # for ext_path in self.config.get('EXTENSIONS', []):
        #     try:
        #         ext = import_string(ext_path)

        #         # TODO: check if ext is a module for safety
        #         if getattr(ext, 'init_app', False):
        #             ext.init_app(self)
        #         else:
        #             ext(self)
        #     except:
        #         raise NoExtensionException(
        #             'No {} extension found'.format(ext_path))
        pass

    def configure_before_request(self):
        pass

    def configure_views(self):
        """You can add some simple views here for fast prototyping."""
        pass
