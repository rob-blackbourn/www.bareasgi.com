"""Using HTTPS with hypercorn"""

import asyncio
import logging
import os.path
import signal
from typing import Any, Dict

from hypercorn.asyncio import serve
from hypercorn.config import Config
import pkg_resources
import uvloop
import yaml

from bareasgi import Application

from bareasgi_web_site.app import create_application

LOGGER = logging.getLogger(__name__)


def _load_config(filename: str) -> Dict[str, Any]:
    with open(filename, 'rt') as file_ptr:
        return yaml.load(file_ptr, Loader=yaml.FullLoader)


def _initialise_logging(config: Dict[str, Any]) -> None:
    if 'logging' in config:
        logging.config.dictConfig(config['logging'])


def _start_hypercorn(app: Application, config: Dict[str, Any]) -> None:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    shutdown_event = asyncio.Event()

    def _signal_handler(*_: Any) -> None:
        shutdown_event.set()
    loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    loop.add_signal_handler(signal.SIGINT, _signal_handler)

    http_config = Config()
    http_config.bind = [f"{config['host']}:{config['port']}"]
    http_config.loglevel = 'debug'
    if config['ssl']['enabled']:
        http_config.certfile = os.path.expandvars(config['ssl']['certfile'])
        http_config.keyfile = os.path.expandvars(config['ssl']['keyfile'])

    loop.run_until_complete(
        serve(
            app,
            http_config,
            shutdown_trigger=shutdown_event.wait  # type: ignore
        )
    )


def start_server():
    """Start the server"""
    config_path = pkg_resources.resource_filename(__name__, "config.yml")
    config = _load_config(config_path)

    _initialise_logging(config)

    assets_path = pkg_resources.resource_filename(__name__, "assets")
    app = create_application(config['app'], assets_path)

    _start_hypercorn(app, config['app'])


if __name__ == '__main__':
    start_server()
