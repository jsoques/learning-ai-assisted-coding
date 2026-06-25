from __future__ import annotations

import secrets

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"
CSRF_FIELD_NAME = "csrf_token"

SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
SKIP_PATHS = frozenset({"/auth/login", "/auth/register", "/auth/logout"})


def _generate_token() -> str:
    return secrets.token_hex(32)


def _get_cookie_token(request: Request) -> str | None:
    return request.cookies.get(CSRF_COOKIE_NAME)


def _get_header_token(request: Request) -> str | None:
    return request.headers.get(CSRF_HEADER_NAME)


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        if not path.startswith("/api/") and request.method not in SAFE_METHODS and path not in SKIP_PATHS:
            cookie_token = _get_cookie_token(request)
            if not cookie_token:
                return HTMLResponse("<h1>CSRF validation failed</h1><p>Missing CSRF cookie.</p>", status_code=403)

            header_token = _get_header_token(request)
            if not header_token or not secrets.compare_digest(header_token, cookie_token):
                return HTMLResponse(
                    "<h1>CSRF validation failed</h1><p>Invalid or missing CSRF token.</p>",
                    status_code=403,
                )

        response: Response = await call_next(request)

        if not path.startswith("/api/"):
            response.set_cookie(
                key=CSRF_COOKIE_NAME,
                value=_generate_token(),
                httponly=False,
                samesite="lax",
                max_age=86400,
            )

        return response
