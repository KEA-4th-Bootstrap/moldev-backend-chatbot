
from pydantic import BaseModel, Field

class ChatBotResponse(BaseModel):
    message: str

class ChatBotRequest(BaseModel):
    moldev_id: int = Field(..., alias='moldevId')
    query: str

