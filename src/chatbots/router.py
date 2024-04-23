from fastapi import APIRouter, status, Query
from src.chatbots import service
from src.chatbots.schemas import ChatBotResponse

router = APIRouter()

@router.get("/{member_id}", status_code=status.HTTP_200_OK, response_model=ChatBotResponse)
async def register_user(member_id: int, query: str = Query(...)):
    print("[API!]", member_id, query)
    await service.save_post_md(member_id)
    result = await service.send_query(member_id, query)
    return {
        "status": status.HTTP_200_OK,
        "message": "요청이 성공했습니다.",
        "data": result
    }
