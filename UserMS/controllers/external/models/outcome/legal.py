from pydantic import BaseModel, Field
from UserMS.core.hydantic.fields import ObjectId


class AddLegalResponseModel(BaseModel):

    id: ObjectId = Field(alias="_id")
