from fastapi import APIRouter, status, Query
from src.chatbots import service
from src.chatbots.schemas import ChatBotResponse, ChatBotRequest

router = APIRouter()

@router.post("", status_code=status.HTTP_200_OK, response_model=ChatBotResponse)
async def send_message(request: ChatBotRequest):
    # 나중에 로그찍는걸로 바꿔도 좋을듯
    print("[INPUT] : member_id - ", request.member_id, " | query - ", request.query)
    await service.save_post_md(request.member_id)
    result = await service.send_query(request.member_id, request.query)
    return {
        "message": result
    }
