from pydantic import BaseModel, Field
from UserMS.core.hydantic.fields import ObjectId


class SetUserOutcome(BaseModel):

    id: ObjectId = Field(..., alias="_id")
