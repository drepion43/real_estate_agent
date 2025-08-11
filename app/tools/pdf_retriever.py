from ntpath import exists
import os
from typing import Type, Sequence
from pydantic import BaseModel, Field

from langchain_core.tools import BaseTool, create_retriever_tool, tool
from langchain_core.documents import Document
from langchain_community.document_loaders import PDFPlumberLoader, PyPDFLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers.multi_vector import MultiVectorRetriever
from unstructured.partition.pdf import partition_pdf
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.storage import InMemoryStore
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

import tiktoken
import requests
import base64
import uuid
from PIL import Image
import re, io
from IPython.display import HTML, display
import hashlib
from pathlib import Path
import pickle
from glob import glob

class PDFRetrievalToolInput(BaseModel):
    user_query: str = Field("사용자의 질문입니다. 사용자는 PDF의 내용과 관련한 질문을 제시합니다.")
    source_uri: str = Field("PDF 파일의 URI입니다.")


class PDFRetrievalTool(BaseTool):
    name: str = "PDF Retrieval"
    description: str = "Retrieve text from a PDF file."
    args_schema: Type[BaseModel] = PDFRetrievalToolInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

    def vectorization(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        docs_splitterd = self.text_splitter.split_documents(docs)

        embeddings = os.getenv("OPENAI_API_EMBEDDINGS", "text-embedding-3-small")
        embeddings = OpenAIEmbeddings(embeddings)
        vector_db = Chroma.from_documents(documents=docs_splitterd, embedding=embeddings)
        

    def load_documents(self, source_uris: Sequence[str]) -> Sequence[Document]:
        docs = []
        for source_uri in source_uris:
            loader = PDFPlumberLoader(source_uri)
            docs.extend(loader.load())
        return docs

@tool
def PDFVectorRetrievalTool(
    question:str,
    announcement_name:str,
    announcement_link:str
    ):
    """
    여러개의 모집공고문과 그 공고문에 접속할 수 있는 외부 링크가 대화 히스토리에 주어집니다.
    사용자가 원하는 모집공고문의 링크를 선택하면, 선택한 링크를 로컬에 다운로드 후 벡터화 한 뒤 사용자 질문에 답변하는 툴입니다.
    
    기존에 이미 다운로드 받은 링크라면, 캐쉬 파일을 이용해 바로 사용자 질문에 답변을 할 수 있습니다.

    Args:
        question (str): 사용자의 질문입니다. 사용자는 PDF의 내용과 관련한 질문을 제시합니다.
        announcement_name (str): 사용자가 원하는 모집공고문의 이름입니다.
        announcement_link (str): 사용자가 원하는 모집공고문에 대한 외부 링크입니다. 이 링크를 통해 로컬에 파일을 다운로드 받습니다. 대화 히스토리에 존재하는 링크입니다.
    """
    def extract_pdf_elements(pdf_path, img_save_path):
        """
        PDF 파일에서 이미지, 테이블, 그리고 텍스트 조각을 추출합니다.
        """

        return partition_pdf(
            filename=pdf_path,                  # mandatory
            strategy="hi_res",                                     # mandatory to use ``hi_res`` strategy
            chunking_strategy="by_title",                        # 이 설정을 줘야 NarrativeText, listItem 등이 CompositeElement 처리 됌.
            languages=["kor"],
            # extract_images_in_pdf=True,                            # mandatory to set as ``True``
            # extract_image_block_types=[
                                    # "Image", 
                                    #"Table"                    # Table까지 하면 이미지 너무 많아져서 분당 최대 요청 Token(20만) 초과함.
                                    # ],          # optional
            # extract_image_block_to_payload=False,                  # optional
            # extract_image_block_output_dir=img_save_path,  # optional - only works when ``extract_image_block_to_payload=False``
        )

    def get_cache_key(announcement_link):
        """PDF 파일의 해시값을 기반으로 캐시 키 생성"""
        # with open(pdf_path, 'rb') as f:       
        file_hash = hashlib.sha256(announcement_link.encode()).hexdigest()

        return f"retriever_{file_hash}"

    def categorize_elements(raw_pdf_elements):
        """
        PDF에서 추출된 요소를 테이블과 텍스트로 분류합니다.
        raw_pdf_elements: unstructured.documents.elements의 리스트
        """
        tables = []  # 테이블 저장 리스트
        texts = []  # 텍스트 저장 리스트
        for element in raw_pdf_elements:
            if "unstructured.documents.elements.Table" in str(type(element)):
                tables.append(str(element))  # 테이블 요소 추가
            elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                texts.append(str(element))  # 텍스트 요소 추가
        return texts, tables

    # 벡터 저장소에 텍스트 저장 및 벡터화
    def vectorize_texts(texts, persist_dir, collection_name):
        """
        텍스트 리스트를 Chroma DB에 벡터화하여 저장합니다.
        
        Args:
            texts (List[str]): 벡터화할 텍스트 리스트
            persist_dir (str): Chroma를 저장할 directory path
            collection_name (str): Chroma 컬렉션 이름
            
        Returns:
            Chroma: 벡터 저장소 객체
        """
        # OpenAI 임베딩 함수 초기화
        embedding_function = OpenAIEmbeddings()
        
        # Chroma DB에 문서 저장 및 벡터화
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=embedding_function,
            collection_name=collection_name,
            persist_directory=persist_dir  # 벡터 저장소를 영구 저장할 디렉토리
        )
        
        # 변경사항을 디스크에 저장
        # vectorstore.persist()
        return vectorstore
        
    def load_retriever(persist_dir, collection_name):
        print(f"기존 벡터 저장소를 불러옵니다: {collection_name}")
        embedding_function = OpenAIEmbeddings()

        vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=persist_dir
        )

        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )

        return retriever

    cache_key = get_cache_key(announcement_link=announcement_link)
    local_pdf_save_dir = f'.retriever_cache/{cache_key}'
    local_pdf_path = f'{local_pdf_save_dir}/{cache_key}.pdf'
    persist_dir = f'{local_pdf_save_dir}'
    local_collection_name = f'chroma_collection'
    cache_f = glob(pathname=persist_dir, recursive=True)

    if cache_f:
        retriever = load_retriever(
            persist_dir=persist_dir, 
            collection_name=local_collection_name
            )
        
        result = retriever.invoke(question)

        # GPT-4o, GPT-4, GPT-3.5-turbo 기준
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        tokens = encoding.encode("".join([document.page_content for document in result]))
        print(f"Retrieve 할 문서 수: {len(result)} \n Retrieve 결과의 Token 수: {len(tokens)}")
        return {"messages": [result]}
    
    os.makedirs(local_pdf_save_dir, exist_ok=True)

    # 새로운 announcement_link에 대해 rag할 경우 pdf 로컬에 다운로드
    ################# pdf oneline url에서 다운로드 받는 코드 ######################
    response = requests.get(announcement_link, stream=True)
    with open(local_pdf_path, 'wb') as f:       # 캐쉬 이름과 pdf 파일 이름을 동일하게
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)
    ###########################################################################

    raw_pdf_elements = extract_pdf_elements(pdf_path=local_pdf_path, img_save_path=local_pdf_save_dir)
    print("PDF 텍스트 요소 추출 완료")

    texts, tables = categorize_elements(raw_pdf_elements)

    # 선택사항: 텍스트에 대해 특정 토큰 크기 적용
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=4000, chunk_overlap=0  # 텍스트를 4000 토큰 크기로 분할, 중복 없음
    )

    joined_texts = " ".join(texts)  # 텍스트 결합
    texts_4k_token = text_splitter.split_text(joined_texts)  # 분할 실행

    vector_store = vectorize_texts(
        texts=texts_4k_token, 
        persist_dir=persist_dir,
        collection_name=local_collection_name)

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    result = retriever.invoke(question)

    # retrieve_result = ''
    # for i in retriever_multi_vector_img.ainvoke(question):
    # for i in result:
    #     content = i.page_content
    #     retrieve_result += content
        # break   # 1개만 넣었음. invoke된 모든 텍스트 넣으면 답변할 때 Context 초과됌.

    return {"messages": [result]}



@tool
def PDFMultiVectorRetrievalTool(question:str, 
                                pdf_url: str
                                ):
    """
    여러개의 공고 중 사용자가 원하는 공고문을 하나 선택하고, 선택한 공고문에 대해 벡터화 한 뒤,
    사용자의 질문에 대한 답변을 찾는 툴입니다.

    Args:
        question (str): 사용자의 질문입니다. 사용자는 PDF의 내용과 관련한 질문을 제시합니다.
        pdf_url (str): PDF 파일이 저장되어있는 로컬 url 입니다.
    """

    def create_multi_vector_retriever(
        vectorstore, text_summaries, texts, table_summaries, tables, image_summaries, images
    ): 
        """
        요약을 색인화하지만 원본 이미지나 텍스트를 반환하는 검색기를 생성합니다.
        """

        # 저장 계층 초기화
        store = InMemoryStore()
        id_key = "doc_id"

        # 멀티 벡터 검색기 생성
        retriever = MultiVectorRetriever(
            vectorstore=vectorstore,        # 요약된 색인을 저장하는 vectorstore
            docstore=store,                 # 원본 이미지, 텍스트, 테이블을 저장하는 docstore
            id_key=id_key,
        )

        # retriever.search_kwargs['k'] = 1      # Retrieve로 가져올 문서 조절

        # 문서를 벡터 저장소와 문서 저장소에 추가하는 헬퍼 함수
        def add_documents(retriever, doc_summaries, doc_contents):
            doc_ids = [
                str(uuid.uuid4()) for _ in doc_contents         # uuid는 고유한 ID 생성을 위해 사용.
                                                                # 이 고유 ID가 vectorstore, docstore에 모두 저장되서 서로 연결됌.
            ]  # 문서 내용마다 고유 ID 생성

            summary_docs = [
                Document(page_content=s, metadata={id_key: doc_ids[i]})
                for i, s in enumerate(doc_summaries)
            ]

            retriever.vectorstore.add_documents(
                summary_docs
            )  # 요약 문서를 벡터 저장소에 추가

            # ✅ 문서 저장소에 추가할 때, Document 객체로 변환하여 저장
            doc_objects = [
                (doc_ids[i], Document(page_content=doc_contents[i]))
                for i in range(len(doc_contents))
            ]
            retriever.docstore.mset(doc_objects)

            # retriever.docstore.mset(
            #     list(zip(doc_ids, doc_contents))
            # )  # 문서 내용을 문서 저장소에 추가

        # 텍스트, 테이블, 이미지 추가
        if text_summaries:
            add_documents(retriever, text_summaries, texts)

        if table_summaries:
            add_documents(retriever, table_summaries, tables)

        if image_summaries:
            add_documents(retriever, image_summaries, images)

        return retriever

    def get_cache_key(pdf_url):
        """PDF 파일의 해시값을 기반으로 캐시 키 생성"""
        # with open(pdf_path, 'rb') as f:       
        file_hash = hashlib.sha256(pdf_url.encode()).hexdigest()

        return f"retriever_{file_hash}"

    def save_chunk_data(cache_key, cache_dir=".retriever_cache", **kwargs):
        cache_path = Path(cache_dir) / cache_key
        cache_path.mkdir(parents=True, exist_ok=True)

        keys = ['text_summaries', 'texts', 'table_summaries', 'tables', 'image_summaries', 'images']
        if all(k in keys for k in kwargs.keys()):
            for k, v in kwargs.items():
                cache_path = Path(cache_dir) / cache_key / (k + ".pkl")
                with open(cache_path, 'wb') as f:
                    pickle.dump(v, f)

        else: raise KeyError(f"{keys}를 반드시 포함해야함")

    def save_retriever(cache_key, retriever, cache_dir=".retriever_cache"):
        """Retriever를 파일로 저장"""
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = Path(cache_dir) / cache_key
        
        with open(cache_path, 'wb') as f:
            pickle.dump(retriever, f)

    def load_retriever(cache_key, cache_dir=".retriever_cache"):
        """파일에서 Retriever 로드"""
        cache_path = Path(cache_dir) / cache_key
        if not cache_path.exists():
            raise ValueError(f"{cache_path} 미 존재")
        
        keys = ['text_summaries', 'texts', 'table_summaries', 'tables', 'image_summaries', 'images']
        caches = {}

        if all([(Path(cache_path) / (k + ".pkl")).exists() for k in keys]):
            for k in keys:
                cache_path = Path(cache_dir) / cache_key / (k + ".pkl")
                with open(cache_path, 'rb') as f:
                    caches[k] = pickle.load(f)
        else:
            raise ValueError(f"{cache_path} 이하에 {keys} 파일 미존재")

        # 요약텍스트를 색인화하기 위해 사용할 벡터 저장소
        vectorstore = Chroma(
            collection_name="sample-rag-multi-modal", embedding_function=OpenAIEmbeddings()
        )


        retriever_multi_vector_img = create_multi_vector_retriever(
            vectorstore=vectorstore,
            text_summaries=caches['text_summaries'],
            texts=caches['texts'],
            table_summaries=caches['table_summaries'],
            tables=caches['tables'],
            image_summaries=caches['image_summaries'],
            images=caches['images']
        )

        return retriever_multi_vector_img

    cache_key = get_cache_key(pdf_url=pdf_url)
    local_pdf_save_dir = f'.retriever_cache/{cache_key}'
    local_pdf_path = f'{local_pdf_save_dir}/{cache_key}.pdf'
    cache_f = glob(pathname=local_pdf_path, recursive=True)

    if cache_f:
        retriever_multi_vector_img = load_retriever(cache_key=cache_key)
        result = retriever_multi_vector_img.invoke(question)
        # GPT-4o, GPT-4, GPT-3.5-turbo 기준
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        tokens = encoding.encode("".join([document.page_content for document in result]))
        print(f"Retrieve 할 문서 수: {len(result)} \n Retrieve 결과의 Token 수: {len(tokens)}")
        return {"messages": [result]}
    
    os.makedirs(local_pdf_save_dir, exist_ok=True)

    # 새로운 pdf_url에 대해 rag할 경우 pdf 로컬에 다운로드
    ################# pdf oneline url에서 다운로드 받는 코드 ######################
    response = requests.get(pdf_url, stream=True)
    with open(local_pdf_path, 'wb') as f:       # 캐쉬 이름과 pdf 파일 이름을 동일하게
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)
    ############################################################################

    def categorize_elements(raw_pdf_elements):
        """
        PDF에서 추출된 요소를 테이블과 텍스트로 분류합니다.
        raw_pdf_elements: unstructured.documents.elements의 리스트
        """
        tables = []  # 테이블 저장 리스트
        texts = []  # 텍스트 저장 리스트
        for element in raw_pdf_elements:
            if "unstructured.documents.elements.Table" in str(type(element)):
                tables.append(str(element))  # 테이블 요소 추가
            elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                texts.append(str(element))  # 텍스트 요소 추가
        return texts, tables
    
    def extract_pdf_elements(pdf_path, img_save_path):
        """
        PDF 파일에서 이미지, 테이블, 그리고 텍스트 조각을 추출합니다.
        """

        # extracted_image_path = os.path.join("./extracted_images")
        # os.makedirs(extracted_image_path, exist_ok=True)

        # return partition_pdf(
        #     filename=pdf_path,
        #     extract_images_in_pdf=True,  # PDF 내 이미지 추출 활성화
        #     infer_table_structure=True,  # 테이블 구조 추론 활성화
        #     chunking_strategy="basic",
        #     # chunking_strategy="by_title",  # by_title로 chunking 하면 max_characters, new_after_n_chars 파라미터가 무시되는걸로 보임.제목별로 텍스트 조각화
        #     max_characters=400,  # 최대 문자 수. 4000
        #     new_after_n_chars=380,  # 이 문자 수 이후에 새로운 조각 생성. 380
        #     combine_text_under_n_chars=200,  # 이 문자 수 이하의 텍스트는 결합. 2000
        #     # image_output_dir_path=path,  # 이미지 출력 디렉토리 경로      # 25.01.28 이 parameter 없는것 같아서 아래 코드 추가.
        #     extract_image_block_output_dir=extracted_image_path,
        # )
    
        # return partition_pdf(
        #     filename=pdf_path,
        #     extract_images_in_pdf=True,  # PDF 내 이미지 추출 활성화
        #     infer_table_structure=True,  # 테이블 구조 추론 활성화1
        #     # chunking_strategy="basic",
        #     chunking_strategy="by_title",  # by_title로 chunking 하면 max_characters, new_after_n_chars 파라미터가 무시되는걸로 보임.제목별로 텍스트 조각화
        #     max_characters=4000,  # 최대 문자 수. 4000
        #     new_after_n_chars=3800,  # 이 문자 수 이후에 새로운 조각 생성. 380
        #     combine_text_under_n_chars=2000,  # 이 문자 수 이하의 텍스트는 결합. 2000
        #     # image_output_dir_path=path,  # 이미지 출력 디렉토리 경로      # 25.01.28 이 parameter 없는것 같아서 아래 코드 추가.
        #     extract_image_block_output_dir=extracted_image_path,
        # )

        return partition_pdf(
            filename=pdf_path,                  # mandatory
            strategy="hi_res",                                     # mandatory to use ``hi_res`` strategy
            chunking_strategy="by_title",                        # 이 설정을 줘야 NarrativeText, listItem 등이 CompositeElement 처리 됌.
            languages=["kor"],
            extract_images_in_pdf=True,                            # mandatory to set as ``True``
            extract_image_block_types=["Image", 
                                    #"Table"                    # Table까지 하면 이미지 너무 많아져서 분당 최대 요청 Token(20만) 초과함.
                                    ],          # optional
            extract_image_block_to_payload=False,                  # optional
            extract_image_block_output_dir=img_save_path,  # optional - only works when ``extract_image_block_to_payload=False``
        )
    
    def generate_text_summaries(texts, tables, summarize_texts=False):
        """
        텍스트 요소 요약
        texts: 문자열 리스트
        tables: 문자열 리스트
        summarize_texts: 텍스트 요약 여부를 결정. True/False
        """

        # 프롬프트 설정
        prompt_text = """You are an assistant tasked with summarizing tables and text for retrieval. \
        These summaries will be embedded and used to retrieve the raw text or table elements. \
        Give a concise summary of the table or text that is well optimized for retrieval. Table or text: {element} """
        prompt = ChatPromptTemplate.from_template(prompt_text)

        # 텍스트 요약 체인
        model = ChatOpenAI(temperature=0, model="gpt-4o-mini", tags=["Summary"])
        summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

        # 요약을 위한 빈 리스트 초기화
        text_summaries = []
        table_summaries = []

        # 제공된 텍스트에 대해 요약이 요청되었을 경우 적용
        if texts and summarize_texts:
            text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})
        elif texts:
            text_summaries = texts

        # 제공된 테이블에 적용
        if tables:
            table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})

        return text_summaries, table_summaries

    def generate_img_summaries(path):
        """
        이미지에 대한 요약과 base64 인코딩된 문자열을 생성합니다.
        path: Unstructured에 의해 추출된 .jpg 파일 목록의 경로
        """

        # base64로 인코딩된 이미지를 저장할 리스트
        img_base64_list = []

        # 이미지 요약을 저장할 리스트
        image_summaries = []

        # 요약을 위한 프롬프트
        prompt = """You are an assistant tasked with summarizing images for retrieval. \
        These summaries will be embedded and used to retrieve the raw image. \
        Give a concise summary of the image that is well optimized for retrieval."""

        # 이미지에 적용
        for img_file in sorted(os.listdir(path)):
            if img_file.endswith(".jpg"):
                img_path = os.path.join(path, img_file)
                base64_image = encode_image(img_path)
                img_base64_list.append(base64_image)
                image_summaries.append(image_summarize(base64_image, prompt))

        return img_base64_list, image_summaries
    
    def image_summarize(img_base64, prompt):
        # 이미지 요약을 생성합니다.
        chat = ChatOpenAI(model="gpt-4o-mini", max_tokens=512, tags=["Summary"])     # max_tokens=2048

        msg = chat.invoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                        },
                    ]
                )
            ]
        )
        return msg.content
    
    def encode_image(image_path):
        # 이미지 파일을 base64 문자열로 인코딩합니다.
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def plt_img_base64(img_base64):
        """base64 인코딩된 문자열을 이미지로 표시"""
        # base64 문자열을 소스로 사용하는 HTML img 태그 생성
        image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'
        # HTML을 렌더링하여 이미지 표시
        display(HTML(image_html))


    def looks_like_base64(sb):
        """문자열이 base64로 보이는지 확인"""
        return re.match("^[A-Za-z0-9+/]+[=]{0,2}$", sb) is not None


    def is_image_data(b64data):
        """
        base64 데이터가 이미지인지 시작 부분을 보고 확인
        """
        image_signatures = {
            b"\xff\xd8\xff": "jpg",
            b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a": "png",
            b"\x47\x49\x46\x38": "gif",
            b"\x52\x49\x46\x46": "webp",
        }
        try:
            header = base64.b64decode(b64data)[:8]  # 처음 8바이트를 디코드하여 가져옴
            for sig, format in image_signatures.items():
                if header.startswith(sig):
                    return True
            return False
        except Exception:
            return False


    def resize_base64_image(base64_string, size=(128, 128)):
        """
        Base64 문자열로 인코딩된 이미지의 크기 조정
        """
        # Base64 문자열 디코드
        img_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_data))

        # 이미지 크기 조정
        resized_img = img.resize(size, Image.LANCZOS)

        # 조정된 이미지를 바이트 버퍼에 저장
        buffered = io.BytesIO()
        resized_img.save(buffered, format=img.format)

        # 조정된 이미지를 Base64로 인코딩
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


    def split_image_text_types(docs):
        """
        base64로 인코딩된 이미지와 텍스트 분리
        """
        b64_images = []
        texts = []
        for doc in docs:
            # 문서가 Document 타입인 경우 page_content 추출
            if isinstance(doc, Document):
                doc = doc.page_content

            if looks_like_base64(doc) and is_image_data(doc):
                # doc = self.resize_base64_image(doc, size=(1300, 600))
                doc = resize_base64_image(doc, size=(128, 128))
                b64_images.append(doc)
            else:
                texts.append(doc)
        return {"images": b64_images, "texts": texts}


    def img_prompt_func(data_dict):
        """
        컨텍스트를 단일 문자열로 결합
        """
        formatted_texts = "\n".join(data_dict["context"]["texts"])
        messages = []

        # 이미지가 있으면 메시지에 추가
        if data_dict["context"]["images"]:
            for image in data_dict["context"]["images"]:
                image_message = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                }
                messages.append(image_message)


    # pdf_path = state["pdf_path"]
    raw_pdf_elements = extract_pdf_elements(pdf_path=local_pdf_path, img_save_path=local_pdf_save_dir)
    texts, tables = categorize_elements(raw_pdf_elements)
    print("PDF 텍스트, 이미지, 테이블 요소 추출, 분류 완료")

    # 선택사항: 텍스트에 대해 특정 토큰 크기 적용
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=4000, chunk_overlap=0  # 텍스트를 4000 토큰 크기로 분할, 중복 없음
    )

    joined_texts = " ".join(texts)  # 텍스트 결합
    texts_4k_token = text_splitter.split_text(joined_texts)  # 분할 실행

    # 텍스트, 테이블 요약 가져오기
    text_summaries, table_summaries = generate_text_summaries(
        texts_4k_token, tables, summarize_texts=True
    )

    img_base64_list, image_summaries = generate_img_summaries(path=local_pdf_save_dir)

    # 요약텍스트를 색인화하기 위해 사용할 벡터 저장소
    vectorstore = Chroma(
        collection_name="sample-rag-multi-modal", embedding_function=OpenAIEmbeddings()
    )

    # 검색기 생성
    retriever_multi_vector_img = create_multi_vector_retriever(
        vectorstore,
        text_summaries,
        texts,
        table_summaries,
        tables,
        image_summaries,
        img_base64_list,
    )

    # save_retriever(cache_key=cache_key, retriever=retriever_multi_vector_img)
    save_chunk_data(cache_key=cache_key, 
        text_summaries = text_summaries,
        texts = texts,
        table_summaries = table_summaries,
        tables = tables,
        image_summaries = image_summaries,
        images = img_base64_list
    )

    result = retriever_multi_vector_img.invoke(question)

    # retrieve_result = ''
    # for i in retriever_multi_vector_img.ainvoke(question):
    # for i in result:
    #     content = i.page_content
    #     retrieve_result += content
        # break   # 1개만 넣었음. invoke된 모든 텍스트 넣으면 답변할 때 Context 초과됌.

    # print(f"완성된 retrieve_result: {retrieve_result}")
    return {"messages": [result]}