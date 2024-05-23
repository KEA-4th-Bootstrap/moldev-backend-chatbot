
from pydantic import BaseModel, Field

class ChatBotResponse(BaseModel):
    message: str

class ChatBotRequest(BaseModel):
    member_id: int = Field(..., alias='memberId')
    query: str

