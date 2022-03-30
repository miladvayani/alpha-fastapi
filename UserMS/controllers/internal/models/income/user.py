from pydantic import BaseModel


class SetUserIncome(BaseModel):

    mobile_number: str
