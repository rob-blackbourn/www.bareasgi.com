"""The Application"""

import os.path
import logging
from typing import Any, Dict, List, Optional

import aiofiles
from bareasgi import (
    Scope,
    Info,
    RouteMatches,
    Content
)
import bareasgi_jinja2
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


@bareasgi_jinja2.template('markdown.html')
async def get_markdown(
        _scope: Scope,
        info: Info,
        matches: RouteMatches,
        _content: Content
) -> Dict[str, Any]:
    """A request handler"""
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
    return {
        'title': 'bareASGI tutorial',
        'md_html': md_html
    }
