"""The Application"""

import os.path
import logging
from typing import List, Optional

import aiofiles
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


async def _get_document(
        path: str,
        doc_folders: List[str]
) -> Optional[str]:
    for folder in doc_folders:
        full_path = os.path.join(folder, path)
        if os.path.exists(full_path):
            break
    else:
        return None

    async with aiofiles.open(full_path, 'rt') as file_ptr:
        return await file_ptr.read()


async def get_markdown(
        _scope: Scope,
        info: Info,
        matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    """A request handler"""
    try:
        config = info['config']
        doc_folders = [os.path.expandvars(path) for path in config['docs']]
        path = matches['docs']
        text = await _get_document(path, doc_folders)
        if not path.endswith('.md'):
            text = f"""
# {path}

```
{text}
```
"""
        md_text = markdown(text, extensions=['extra', 'codehilite'])
        md_html = markdown(md_text)

        html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>bareASGI</title>
    <link rel="shortcut icon" href="/assets/favicon.ico" type="image/x-icon">    
    <link href="//cdn.muicss.com/mui-0.10.0/css/mui.min.css" rel="stylesheet" type="text/css" />
    <script src="//cdn.muicss.com/mui-0.10.0/js/mui.min.js"></script>
    <link rel="stylesheet" type="text/css" href="/assets/codehilite.css">
  </head>
  <body>
    <div class="mui-container-fluid">
      <div class="mui-panel">
        {md_html}
      </div>
    </div>
  </body>
</html>
"""
        return 200, [(b'content-type', b'text/html')], text_writer(html)
    except Exception as error:  # pylint: disable=bare-except
        return 500
