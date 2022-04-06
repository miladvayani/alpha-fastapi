from .interfaces import JsonifierInterface
from .types import ModuleType
from .interfaces import ModelInterface

class Jsonifier(JsonifierInterface):

    def _serializer(self, data: dict) -> str:
        return self.jsonify.dumps(data)

    def _deserializer(self, data: str) -> dict:
        serialized = self._serializer(data)
        return self.jsonify.loads(serialized)