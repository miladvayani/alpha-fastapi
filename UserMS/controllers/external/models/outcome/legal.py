from pydantic import BaseModel, Field
from UserMS.core.contrib import fields


class AddLegalResponseModel(BaseModel):

    id: fields.ObjectId = Field(alias="_id")
