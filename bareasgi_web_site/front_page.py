"""The Application"""

from typing import Any, Dict
import logging

from bareasgi import (
    Scope,
    Info,
    RouteMatches,
    Content
)
import bareasgi_jinja2

LOGGER = logging.getLogger(__name__)


@bareasgi_jinja2.template('index.html')
async def get_frontpage(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> Dict[str, Any]:
    """A request handler"""
    return {
        'title': 'bareASGI'
    }


@bareasgi_jinja2.template('why.html')
async def get_why(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> Dict[str, Any]:
    """A request handler"""
    return {
        'title': 'bareASGI'
    }
