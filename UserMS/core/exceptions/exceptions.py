import ast
from typing import Iterable
from ..responses.responses import Response
from ..proxies import message as messages
from ..i18n import _
from pymongo.errors import DuplicateKeyError
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError


async def base_exception_handler(request: Request, e: HTTPException):
    get_flashed_messages = messages.get_private_stack()
    if not get_flashed_messages:
        messages(e.detail)
    return Response(status_code=e.status_code)


async def http_500_error_handler(request: Request, exc: Exception):
    messages("Internal Server Error")
    return Response(status_code=500)


async def http_duplicate_error_handler(request: Request, exc: DuplicateKeyError):
    get_flashed_messages = messages.get_private_stack()
    if not get_flashed_messages:
        errors = [
            {key: _("This field is duplicate")}
            for key in exc.details["keyValue"].keys()
        ]
        messages(errors)
    return Response(status_code=402)


async def http_422_error_handler(request: Request, exc: RequestValidationError):
    """
    Handler for 422 error to transform default pydantic error object to custom format
    """
    exc2 = ast.literal_eval(exc.json())
    errors = {}
    if isinstance(exc2, Iterable):
        for error in exc2:
            # get error keys
            error_names = [i for i in error["loc"][1:]]
            # temp dictionary for generating each error as embeded one
            temp_dict = {}
            # asign error message with last key in error list
            if error_names:
                temp_dict[error_names[-1]] = error["msg"]
                # generate or add new errors for final errors
                errors = generate_error_dict(error_names, errors, temp_dict)
            else:
                messages("Invalid request body")
    messages(errors)
    return Response(status_code=400)


def generate_error_dict(error_arr: list, errors_dict: dict, temp_dict: dict) -> dict:
    """A recursive function for iterate on dictionary and match key values

    Args:
        error_arr (list): list of error list
        errors_dict (dict): dictionary of errors
        temp_dict (dict): temp dict of error values for matching with error key

    Returns:
        dict: value of error key for update or add new one
    """
    if error_arr[0] in errors_dict.keys():  # if a key matches with errors key
        # remove first element of errors list for send to function again and checks for matching
        temp = error_arr[0]
        del error_arr[0]
        # update error key with new value error
        errors_dict.update(
            {temp: generate_error_dict(error_arr, errors_dict[temp], temp_dict)}
        )
    else:  # if not a key matches with error dict, generate value for matched key
        # iterate on unmatched keys and generate new error value
        for i in range(len(error_arr) - 2, -1, -1):
            temp_dict = {error_arr[i]: temp_dict}
        errors_dict.update(temp_dict)
    return errors_dict
