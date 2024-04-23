
from pydantic import BaseModel

class ChatBotResponse(BaseModel):
    status: int
    message: str
    data: str

