
from pydantic import BaseModel, Field

class ChatBotResponse(BaseModel):
    message: str

class ChatBotRequest(BaseModel):
    moldev_id: str = Field(..., alias='moldevId')
    query: str

