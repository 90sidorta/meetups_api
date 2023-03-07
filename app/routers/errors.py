from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute


class RouteErrorHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as ex:
                if isinstance(ex, HTTPException):
                    raise ex
                raise HTTPException(status_code=500, detail=str(ex))

        return custom_route_handler
