"""The Application"""

import logging

from bareasgi import (
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpResponse,
    text_writer
)

LOGGER = logging.getLogger(__name__)


async def get_frontpage(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    """A request handler"""
    try:
        html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>bareASGI</title>
    <link rel="shortcut icon" href="/assets/favicon.ico" type="image/x-icon">    
    <link href="//cdn.muicss.com/mui-0.10.0/css/mui.min.css" rel="stylesheet" type="text/css" />
    <script src="//cdn.muicss.com/mui-0.10.0/js/mui.min.js"></script>
    <link rel="stylesheet" type="text/css" href="/assets/mui-style.css">
    <link rel="stylesheet" type="text/css" href="/assets/codehilite.css">
  </head>
  <body>
    <header class="mui-appbar mui--z1">
      <div class="mui-container">
        <table>
          <tr class="mui--appbar-height">
            <td class="mui--text-title">
              <a href="/">
                <img
                  src="/assets/peach.svg"
                  alt="It's a peach"
                  width="32px" height="32px"
                />
              </a>
            </td>
            <td align="mui--text-right">
              <ul class="mui-list--inline mui--text-body2">
                <li>
                  <a href="/tutorial/docs/table-of-contents.md">
                    tutorial
                  </a>
                </li>
              </ul>
            </td>
          </tr>
        </table>
      </div>
    </header>
    <div id="content-wrapper" class="mui--text-center">
      <div class="mui--appbar-height"></div>
      <br>
      <br>
      <div class="mui--text-display3">bareASGI</div>
      <br>
      <br>
      <button class="mui-btn mui-btn--raised">Get started</button>
    </div>
    <footer>
      <div class="mui-container mui--text-center">
        Powered by bareASGI!
      </div>
    </footer>
  </body>
</html>
"""
        return 200, [(b'content-type', b'text/html')], text_writer(html)
    except Exception as error:  # pylint: disable=bare-except
        return 500
