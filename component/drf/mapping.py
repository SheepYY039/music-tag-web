# -*- coding: utf-8 -*-
from component.utils.exceptions import (
    AuthenticationError,
    MethodNotAllowedError,
    NotAcceptableError,
    NotAuthenticatedError,
    ParamValidationError,
    PermissionDeniedError,
    ResourceNotFound,
    ThrottledError,
    UnsupportedMediaTypeError,
)

# drf exception to blueapps exception
exception_mapping = {
    "ValidationError": ParamValidationError,
    "AuthenticationFailed": AuthenticationError,
    "NotAuthenticated": NotAuthenticatedError,
    "PermissionDenied": PermissionDeniedError,
    "NotFound": ResourceNotFound,
    "MethodNotAllowed": MethodNotAllowedError,
    "NotAcceptable": NotAcceptableError,
    "UnsupportedMediaType": UnsupportedMediaTypeError,
    "Throttled": ThrottledError,
}
