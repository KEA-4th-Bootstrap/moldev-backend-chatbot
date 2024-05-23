
from pydantic import BaseModel

class ChatBotResponse(BaseModel):
    message: str

