import functools
import inspect

from fastapi import (
    Request, WebSocket, Response,
)
from fastapi.security import SecurityScopes
from starlette.requests import HTTPConnection
from starlette.background import BackgroundTasks as StarletteBackgroundTasks

FASTAPI_DEFAULT_INJECTIONS = [Request, WebSocket, HTTPConnection, Response, StarletteBackgroundTasks, SecurityScopes]


def inject(**dependencies):
    def di_wrapper(f):
        def func_wrapper(*args, **kwargs):
            # Do something with request
            return functools.partial(f, *args, **kwargs)

        injection_params = [
            inspect.Parameter(
                p_name, kind=inspect.Parameter.KEYWORD_ONLY, default=p_value, annotation=type(p_value)
            )
            for p_name, p_value in dependencies.items()
        ]

        handler_signature = inspect.signature(f)
        f_params = [
            param
            for param in handler_signature.parameters.values()
            if param.annotation in FASTAPI_DEFAULT_INJECTIONS
        ]

        merged_parameters = injection_params
        for f_param in f_params:
            for i_param in merged_parameters:
                if f_param.name == i_param.name:
                    break
            else:
                merged_parameters.append(f_param)

        ordered_parameters = sorted(merged_parameters, key=lambda p: p.kind)

        func_wrapper.__signature__ = handler_signature.replace(
            parameters=ordered_parameters, return_annotation=inspect.signature(f).return_annotation
        )

        return func_wrapper

    return di_wrapper
