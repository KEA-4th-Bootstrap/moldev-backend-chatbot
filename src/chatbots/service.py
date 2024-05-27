from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import boto3
from dotenv import load_dotenv
import os

load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

# S3 초기설정
client = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=aws_region
                      )

async def send_query(moldev_id: str, query: str):
    query += ', 반드시 한국말로 대답해줘'
    documents = SimpleDirectoryReader(
        input_files=['./post-md/' + moldev_id + '.md']
    ).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    answer = query_engine.query(query)
    return answer.response

async def save_post_md(moldev_id: str):
    bucket_name = 'moldev-s3-bucket'
    file_key = 'post/' + moldev_id + '_posts.md'
    download_path = './post-md/' + moldev_id + '.md'
    client.download_file(bucket_name, file_key, download_path)
