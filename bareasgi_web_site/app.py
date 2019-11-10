"""The Application"""

import logging
from typing import Any, Dict

from bareasgi import Application
from bareasgi_static import add_static_file_provider

from .markdown_handler import get_markdown
from .front_page import get_frontpage

LOGGER = logging.getLogger(__name__)


def create_application(
        config: Dict[str, Any],
        assets_path: str
) -> Application:
    """Create the aplication"""
    info = {
        'config': config,
        'assets_path': assets_path
    }
    app = Application(info=info)

    app.http_router.add({'GET'}, '/', get_frontpage)
    app.http_router.add({'GET'}, '/tutorial/{docs:path}', get_markdown)

    add_static_file_provider(
        app,
        source_folder=assets_path,
        mount_point='/assets/'
    )

    return app
