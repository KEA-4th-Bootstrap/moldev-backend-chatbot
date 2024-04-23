from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import ServiceContext, set_global_service_context
import os
from dotenv import load_dotenv
from src.chatbots.router import router as chatbot_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    load_dotenv()
    open_api_key = os.getenv('OPENAI_API_KEY')
    open_api_version = os.getenv('OPENAI_API_VERSION')
    azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    open_ai_model = os.getenv('OPENAI_MODEL')
    open_ai_embedding_model = os.getenv('OPENAI_EMBEDDING_MODEL')
    open_ai_model_name = os.getenv('OPENAI_MODEL_DEPLOYMENT_NAME')
    open_ai_embedding_model_name = os.getenv('OPENAI_EMBEDDING_MODEL_DEPLOYMENT_NAME')

    llm = AzureOpenAI(
        model=open_ai_model,
        engine=open_ai_model,
        deployment_name=open_ai_model_name,
        api_key=open_api_key,
        azure_endpoint=azure_openai_endpoint,
        api_version=open_api_version,
    )

    # 모델 생성
    embed_model = AzureOpenAIEmbedding(
        model=open_ai_embedding_model,
        engine=open_ai_embedding_model,
        deployment_name=open_ai_embedding_model_name,
        api_key=open_api_key,
        azure_endpoint=azure_openai_endpoint,
        api_version=open_api_version,
    )

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )

    set_global_service_context(service_context)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/chatbots/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"result": "੯•́ʔ̋ ͙͛*͛ ͙͛*͛ ͙͛̋و"}


app.include_router(chatbot_router, prefix="/api/chatbots", tags=["Chatbot"])