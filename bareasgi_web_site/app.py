"""The Application"""

import logging
from typing import Any, Dict

from bareasgi import Application
from bareasgi_static import add_static_file_provider
import bareasgi_jinja2
import jinja2
import pkg_resources

from .markdown_handler import get_markdown
from .front_page import get_frontpage, get_why

LOGGER = logging.getLogger(__name__)


def create_application(
        config: Dict[str, Any],
        assets_path: str
) -> Application:
    """Create the application"""
    info = {
        'config': config,
        'assets_path': assets_path
    }
    app = Application(info=info)

    app.http_router.add({'GET'}, '/', get_frontpage)
    app.http_router.add({'GET'}, '/why', get_why)
    app.http_router.add({'GET'}, '/tutorial/{docs:path}', get_markdown)

    add_static_file_provider(
        app,
        source_folder=assets_path,
        mount_point='/assets/'
    )

    templates = pkg_resources.resource_filename(__name__, "templates")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates),
        # autoescape=jinja2.select_autoescape(['html', 'xml']),
        enable_async=True
    )
    bareasgi_jinja2.add_jinja2(app, env)

    return app
