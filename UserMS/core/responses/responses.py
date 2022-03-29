from typing import Any
from fastapi.responses import UJSONResponse
from ..proxies.proxies import message
from ujson import dumps
from pydantic.error_wrappers import ValidationError


class ResponseObject:
    def __new__(
        cls, data: Any = None, detail: Any = None, status_code: int = 200
    ) -> Any:
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
        message(dict(status_code=status_code))
        return data


class Response(UJSONResponse):
    media_type = "application/json"

    def dumps(self, content):
        result: bool = True
        prepared_messages: list = message.get_private_stack()
        btsatus: int = None
        if not (self.status_code >= 200 and self.status_code < 300):
            result = False
        final_msgs = dict()
        validations = dict()
        for m in prepared_messages:
            if isinstance(m, dict):
                if "status_code" in m:
                    btsatus = m["status_code"]
                    break
                general = m.get("general", None)
                if general:
                    final_msgs.update(m)
                else:
                    validations.update(m)
            else:
                final_msgs.update({"general": m})
        final_msgs.update({"validations": validations}) if validations else None
        data = dict(
            data=content,
            result=result,
            message=final_msgs,
            status_code=btsatus if btsatus else self.status_code,
        )
        return dumps(data).encode("utf-8")

    def render(self, content: Any) -> bytes:
        return self.dumps(content)
