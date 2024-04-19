from fastapi import FastAPI, Query
import boto3
import os
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, set_global_service_context
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins에는 protocal, domain, port만 등록한다.
origins = [
    "*" # private 영역에서 사용한다면 *로 모든 접근을 허용할 수 있다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)

@app.on_event("startup")
async def startup_event():
    global client

    load_dotenv()
    open_api_key = os.getenv('OPENAI_API_KEY')
    open_api_version = os.getenv('OPENAI_API_VERSION')
    azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

    llm = AzureOpenAI(
        model="gpt-35-turbo-16k-0613",
        deployment_name="moldev-gpt",
        api_key=open_api_key,
        azure_endpoint=azure_openai_endpoint,
        api_version=open_api_version,
    )

    # 모델 생성
    embed_model = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name="moldev-embedding",
        api_key=open_api_key,
        azure_endpoint=azure_openai_endpoint,
        api_version=open_api_version,
    )

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )

    set_global_service_context(service_context)
    print("Initial setup...")
    # 필요한 초기화 코드를 여기에 추가
    # 예: 데이터베이스 연결, 외부 서비스와의 연동, 설정 파일 로드 등

    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION')

    # S3 초기설정
    client = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region
                          )
    print("[END SETTING]")
def send_query(member_id: int, query: str):
    query += ', 반드시 한국말로 대답해줘'
    documents = SimpleDirectoryReader(
        input_files=['./post-md/' + str(member_id) + '.md']
    ).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    answer = query_engine.query(query)
    return answer.response

def save_post_md(member_id):
    global client
    bucket_name = 'moldev-s3-bucket'
    file_key = 'post-md/' + str(member_id) + '.md'
    download_path = 'post-md/' + str(member_id) + '.md'
    client.download_file(bucket_name, file_key, download_path)
    print("[DOWNLOAD COMPLETE] : ")


@app.get("/api/health-check")
async def root():
    return {"੯•́ʔ̋ ͙͛*͛ ͙͛*͛ ͙͛̋و"}


@app.get("/api/chatbots/{member_id}")
async def say_hello(member_id: int, query: str = Query(...)):
    save_post_md(member_id)
    response = send_query(member_id, query)
    return {"message": response}
