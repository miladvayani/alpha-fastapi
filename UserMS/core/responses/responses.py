import ast
from typing import Any
from fastapi.responses import UJSONResponse
from ..proxies.proxies import message
from ujson import dumps
from pydantic.error_wrappers import ValidationError


class ResponseObject:
    def __new__(cls, data: Any = None, detail: Any = None) -> Any:
        """This is a response object that get message and data, then
        return only data and push detail to message proxy.

        Args:
            data (Any): response data.
            detail (Any): response message.

        Returns:
            Any: response data.
        """
        if detail:
            message(detail)
        return data


class Response(UJSONResponse):
    media_type = "application/json"

    def dumps(self, content):
        result: bool = True
        prepared_messages: list = message.get_private_stack()
        if self.status_code != 200:
            result = False

        final_msgs = dict()
        validations = dict()
        for m in prepared_messages:
            if isinstance(m, ValidationError):
                for e in ast.literal_eval(m.json()):
                    validations.update({e["loc"][0]: e["msg"]})
            elif isinstance(m, dict):
                general = m.get("general", None)
                if general:
                    final_msgs.update(m)
                else:
                    validations.update(m)
            else:
                final_msgs.update({"general": m})
        final_msgs.update({"validations": validations}) if validations else None
        data = dict(
            data=content, result=result, message=final_msgs, status=self.status_code
        )
        return dumps(data).encode("utf-8")

    def render(self, content: Any) -> bytes:
        return self.dumps(content)
