"""The Application"""

import os.path
import logging

from bareasgi import (
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
    """A request handler"""
    try:
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
                text = f"""
# {path}

```
{text}
```
"""
            md = markdown(text, extensions=['extra', 'codehilite'])
            md_html = markdown(md)

        html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Hypercorn http</title>
    <!--
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500" rel="stylesheet">
    <link href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css" rel="stylesheet">
    <script src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" type="text/css" href="/assets/codehilite.css">
    -->
    <link href="//cdn.muicss.com/mui-0.10.0/css/mui.min.css" rel="stylesheet" type="text/css" />
    <script src="//cdn.muicss.com/mui-0.10.0/js/mui.min.js"></script>
    <link rel="stylesheet" type="text/css" href="/assets/codehilite.css">
  </head>
  <body>
    <div class="mui-container">
      <div class="mui-panel">
        {md_html}
      </div>
    </div>
  </body>
</html>
"""
        return 200, [(b'content-type', b'text/html')], text_writer(html)
    except:  # pylint: disable=bare-except
        return 500
