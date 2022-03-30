from pydantic import BaseModel, Field
from UserMS.core.contrib import fields


class SetUserOutcome(BaseModel):

    id: fields.ObjectId = Field(..., alias="_id")
