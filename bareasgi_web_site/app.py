"""The Application"""

import os.path
import logging
from typing import Any, Dict

from bareasgi import (
    Application,
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpResponse,
    text_writer
)
from markdown import markdown

LOGGER = logging.getLogger(__name__)


async def get_markdown(
        _scope: Scope,
        info: Info,
        matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    try:
        """A request handler"""
        config = info['config']
        docs_folders = [os.path.expandvars(path) for path in config['docs']]
        path = matches['docs']
        for folder in docs_folders:
            full_path = os.path.join(folder, path)
            if os.path.exists(full_path):
                break
        else:
            return 404

        with open(full_path, 'rt') as file_ptr:
            text = file_ptr.read()
            if not full_path.endswith('.md'):
                text = '```\n\n' + text + '\n```'
            md = markdown(text)
            md_html = markdown(md)

        html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Hypercorn http</title>
  </head>
  <body>
    {md_html}
  </body>
</html>
"""
        return 200, [(b'content-type', b'text/html')], text_writer(html)
    except:
        return 500


def create_application(config: Dict[str, Any]) -> Application:
    app = Application(info={'config': config})
    app.http_router.add({'GET'}, '/doc/{docs:path}', get_markdown)
    return app
