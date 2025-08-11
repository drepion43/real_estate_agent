import asyncio
from law_tool import lawPDF
import traceback
from mcp.server.fastmcp import FastMCP
import sys
import requests
import urllib.parse
from typing import List, Optional
from mcp_server_rag import create_retriever
import os
from glob import glob
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

mcp = FastMCP("law_tool_KOR")
law_pdf = lawPDF()

@mcp.tool()
async def pdf_url(query: str):
    try:
        print(f"pdf url tool : {query}")
        results = await law_pdf.download_pdf_url(query=query)
        print(results)
        return results
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return f"An error occurred while searching: {str(e)}"

# @mcp.tool()
# async def load_pdf(query: str):
#     try:
#         results = await law_pdf.read_content(query=query)
#         return results
#     except Exception as e:
#         traceback.print_exc(file=sys.stderr)
#         return f"An error occurred while searching: {str(e)}"

# @mcp.tool()
# async def download_pdf(pdf_urls: List,
#                        output_dir: str):
#     # print(pdf_urls, output_dir)
    
#     file_paths = []
#     for pdf_url in pdf_urls:
#         file_name = urllib.parse.unquote(pdf_url.split('/')[-1])
#         response = requests.get(pdf_url)
#         output_path = f'{output_dir}/{file_name}'
#         with open(output_path, 'wb') as file:
#             file.write(response.content)
#         file_paths.append(output_path)
#     return file_paths

@mcp.tool()
async def retrieve(question: str,
                   pdf_path: str):
    
    file_name = urllib.parse.unquote(pdf_path.split('/')[-1])
    response = requests.get(pdf_path)
    output_path = f'./downloaded/{file_name}'
    with open(output_path, 'wb') as file:
        file.write(response.content)
    print("pdf 다운 완료")
    
    # if len(pdf_paths) == 0:
    #     directory = "/data/pdf/"
    #     file_pattern = "**/*"
    #     regex_pattern = re.compile(re.escape(question), re.IGNORECASE)  # 대소문자 구분 없는 정규 표현식
    #     files = glob(os.path.join(directory, file_pattern), recursive=True)
    #     pdf_paths = [file for file in files if regex_pattern.search(file)]
        
    retriever = create_retriever(file_path=output_path)
    relevant_docs = retriever.get_relevant_documents(question)
    return "\n".join([doc.page_content for doc in relevant_docs])

if __name__ == "__main__":
    mcp.run(transport="stdio")