import os
import copy
import hashlib
import base64
import asyncio
from typing import Optional, Sequence
from concurrent.futures import ThreadPoolExecutor

from langchain_core.tools import create_retriever_tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.documents import Document

from langgraph.types import Checkpointer
from langgraph.store.base import BaseStore
from langgraph.graph import StateGraph
from langgraph.utils.runnable import RunnableCallable

from ..base_agent.service import BaseAgent
from .schema import PDFAgentState, PDFAgentConfig
from tools.tavily import TavilySearch

from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element
from tools import PDFMultiVectorRetrievalTool, PDFVectorRetrievalTool
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class PDFAgent(BaseAgent):

    retriever_tool_description = (
        "사용자의 질문에 답변할 수 있는 vectorstore를 탐색하는 도구입니다."
        " vectorstore는 대한민국의 아파트 청약 및 청년주택 모집 공고의 내용을 찾을 수 있거나,"
        " 부동산 계약과 관련한 내용을 찾을 수 있습니다."
        " 사용자의 질문이 아파트 청약, 청년주택 모집 공고, 부동산 계약과 관련한 질문이라면,"
        " 해당 vectorstore를 참조하십시오."
    )

    multi_retriever_tool_description = (
        "사용자의 질문에 답변할 수 있는 vectorstore를 탐색하는 도구입니다."
        " vectorstore는 대한민국의 아파트 청약 및 청년주택 모집 공고의 내용을 찾을 수 있거나,"
        " 부동산 계약과 관련한 내용을 찾을 수 있습니다."
        " 사용자의 질문이 아파트 청약, 청년주택 모집 공고, 부동산 계약과 관련한 질문이라면,"
        " 해당 vectorstore를 참조하십시오."
    )
    vectorstore = None
    multi_retriever = None

    def __init__(
        self,
        checkpointer: Optional[Checkpointer] = None,
        store: Optional[BaseStore] = None,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        # self.vectorstore = None
        super().__init__(checkpointer=checkpointer, store=store)

    def init_tools(self):
        tools = [
            # TavilySearch(),
            # PDFMultiVectorRetrievalTool
            PDFVectorRetrievalTool
        ]
        
        if self.multi_retriever is not None:
            retriever_tool = create_retriever_tool(
                self.multi_retriever,
                name="multi_vector_retriever",
                description=self.multi_retriever_tool_description,
                response_format="content_and_artifact",
            )
            tools.append(retriever_tool)

        if self.vectorstore is not None:
            retriever_tool = create_retriever_tool(
                self.vectorstore.as_retriever(),
                name="vectorstore",
                description=self.retriever_tool_description,
                response_format="content_and_artifact",
            )
            tools.append(retriever_tool)

        return tools

    def vectorize(self, state: PDFAgentState, config: PDFAgentConfig) -> PDFAgentState:
        pdf_path = config["pdf_path"]
        docs = []
        for f in pdf_path:
            loader = PyPDFLoader(f)
            docs += loader.load()
        docs_splitterd = self.text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(check_embedding_ctx_length=False, model=os.getenv("OPENAI_API_EMBEDDINGS"))
        self.vectorstore = Chroma.from_documents(documents=docs_splitterd, embedding=embeddings)

        self.__init__(self.workflow.checkpointer, self.workflow.store)
        path_mess = ["* " + os.path.basename(fp) for fp in pdf_path]
        path_mess = "\n".join(path_mess)
        mess = AIMessage(content=(
            "I have successfully vectorized the documents"
            f" from pdf files named:"
            f" \n{path_mess}\n\n"
            " You can now ask me questions about them."
        ))
        return {"messages": [mess]}

    async def avectorize(self, state: PDFAgentState, config: PDFAgentConfig) -> PDFAgentState:
        pdf_path = config["pdf_path"]
        docs = []
        for f in pdf_path:
            loader = PyPDFLoader(f)
            docs += loader.load()
        docs_splitterd = self.text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(check_embedding_ctx_length=False, model=os.getenv("OPENAI_API_EMBEDDINGS"))
        self.vectorstore = await Chroma.afrom_documents(documents=docs_splitterd, embedding=embeddings)

        self.__init__(self.workflow.checkpointer, self.workflow.store)
        path_mess = ["* " + os.path.basename(fp) for fp in pdf_path]
        path_mess = "\n".join(path_mess)
        mess = AIMessage(content=(
            "I have successfully vectorized the documents"
            f" from pdf files named:"
            f" \n{path_mess}\n\n"
            " You can now ask me questions about them."
        ))
        return {"messages": [mess]}

    async def avectorize_multi_vector_retrieve(self, state: PDFAgentState, config: PDFAgentConfig):

        pdf_path = config["pdf_path"]
        id_key = "doc_id"

        collection_hash, elements = await _apartition_pdf(pdf_path)
        documents = await _extract_elements(elements, id_key)

        doc_contents = []
        doc_summaries = []
        for doc in documents:
            retrieve_id = doc.metadata[id_key]
            if "image_base64" in doc.metadata:
                # Image or Table
                doc_summaries.append(doc)
                mset = copy.deepcopy(doc)
                mset.page_content = doc.metadata["image_base64"]
                doc_contents.append((retrieve_id, mset))
            else:
                doc_summaries.append(doc)
                doc_contents.append((retrieve_id, doc))

        # 요약텍스트를 색인화하기 위해 사용할 벡터 저장소
        embeddings = OpenAIEmbeddings(
            check_embedding_ctx_length=False,
            model=os.getenv("OPENAI_API_EMBEDDINGS", "text-embedding-3-small")
        )
        vectorstore = Chroma(
            collection_name=collection_hash,
            embedding_function=embeddings,
        )
        retriever = MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=InMemoryStore(),
            id_key=id_key,
        )

        await retriever.vectorstore.aadd_documents(doc_summaries)
        await retriever.docstore.amset(doc_contents)

        self.multi_retriever = retriever

        self.__init__(self.workflow.checkpointer, self.workflow.store)
        state["messages"].append(
            AIMessage(content=f"I have successfully vectorized the documents from pdf file named {pdf_path}. You can now ask me questions about them.")
        )
        return state

    def init_workflow(self):
        workflow = StateGraph(PDFAgentState)
        # Define the two nodes we will cycle between
        workflow.add_node("agent", RunnableCallable(self.call_model, self.acall_model))
        workflow.add_node("tools", self.tool_node)
        # workflow.add_node("grade_documents", self.grade_docs_node)
        # workflow.add_node("transform_query", self.transform_query)

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.set_entry_point("agent")

        workflow.add_edge("tools", "agent")
        workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`,
            # This means these are the edges taken after the `agent node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            self._should_continue,
        )
        # workflow.add_edge("tools", "grade_documents")
        # workflow.add_conditional_edges(
        #     "grade_documents",
        #     self._decide_to_generate,
        # )
        # workflow.add_edge("transform_query", "agent")

        return workflow


def _preprocess_pdf(fp):
    f_hash = hashlib.sha1(os.path.basename(fp).encode()).hexdigest()
    img_dir = os.path.join(f"./pdf_assets/{f_hash}")
    os.makedirs(img_dir, exist_ok=True)

    return f_hash, partition_pdf(
        filename=fp,
        extract_images_in_pdf=True,  # PDF 내 이미지 추출 활성화
        extract_image_block_output_dir=img_dir,
        extract_image_block_types=["Image", "Table"],
        # infer_table_structure=True,  # 테이블 구조 추론 활성화
        # chunking_strategy="by_title",  # 제목별로 텍스트 조각화
        max_characters=1024,  # 최대 문자 수
        new_after_n_chars=1000,  # 이 문자 수 이후에 새로운 조각 생성
        combine_text_under_n_chars=500,  # 이 문자 수 이하의 텍스트는 결합
        # image_output_dir_path=path,  # 이미지 출력 디렉토리 경로      # 25.01.28 이 parameter 없는것 같아서 아래 코드 추가.
        languages=["eng", "kor"],
    )


async def _apartition_pdf(file_paths: list[str]):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        tasks = [
            loop.run_in_executor(executor, _preprocess_pdf, fp)
            for fp in file_paths
        ]
        elements = await asyncio.gather(*tasks)
    f_hashs = []
    results = []
    for f_hash, elem in elements:
        f_hashs.append(f_hash)
        results += elem
    return "-".join(f_hashs), results


def _preprocess_element(elem: Element, id_key: str) -> Document:
    if elem.category == "Image":
        img = open(elem.metadata.image_path, "rb").read()
        img = base64.b64encode(img).decode("utf-8")
        img_content = _image_summarize(img)
        doc = Document(
            page_content=img_content,
            id=elem.id,
            metadata={
                id_key: elem.id,
                "image_path": elem.metadata.image_path,
                "image_base64": img,
                # "coordinates": elem.metadata.coordinates.points,
            }
        )
        # line = f"<Image {elem.metadata.image_path}></Image>"
    elif elem.category == "Table":
        img = open(elem.metadata.image_path, "rb").read()
        img = base64.b64encode(img).decode("utf-8")
        doc = Document(
            page_content=elem.text,
            id=elem.id,
            metadata={
                id_key: elem.id,
                "image_path": elem.metadata.image_path,
                "image_base64": img,
                # "coordinates": elem.metadata.coordinates.points,
            }
        )
        # line = f"<Table {elem.metadata.image_path}>{elem.text}</Table>"
    else:
        doc = Document(page_content=elem.text, id=elem.id, metadata={id_key: elem.id})

    return doc


async def _extract_elements(elements: Sequence[Element], id_key: str) -> list[Document]:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [
            loop.run_in_executor(executor, _preprocess_element, elem, id_key)
            for elem in elements
        ]
        documents = await asyncio.gather(*tasks)
    return documents


def _image_summarize(img_base64: str):
    instruction = """You are an assistant tasked with summarizing images for retrieval. \
These summaries will be embedded and used to retrieve the raw image. \
Give a concise summary of the image that is well optimized for retrieval. \
Please keep your response in KOREAN."""

    model = ChatOpenAI(model=os.getenv("OPENAI_API_MODEL"), temperature=0)

    msgs = [
        SystemMessage(content=[{"type": "text", "text": instruction}]),
        HumanMessage(
            content=[
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
            ]
        ),
    ]
    response = model.invoke(msgs)
    return response.content


if __name__ == "__main__":
    from langgraph.checkpoint.memory import MemorySaver
    from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
    from dotenv import load_dotenv
    load_dotenv()

    agent = PDFAgent(checkpointer=MemorySaver())

    state = PDFAgentState(
        messages=[
            HumanMessage(content="내가 제시하는 문서는 어떤 아파트 청약 공고문이야, 이 내용에 대해 이야기하고 싶어"),
        ],
        # is_last_step=False,
        remaining_steps=2,
        # pdf_path = "/workspace/LLM/real-estate-agent/app/api/pdf_agent/교대역푸르지오2pages.pdf",
        rewrite_cnt=0,
    )
    config = {
        "configurable": {
            "thread_id": "thread-1",
            "user_id": "user-1",
        },
        "pdf_path": [
            # "./pdf_assets/Gyo-Dae Station Prugio.pdf",
            "./pdf_assets/Gyo-Dae Station Prugio 3 Pages.pdf",
            # "./pdf_assets/리스트안암 24페이지.pdf",
        ],
    }
    # state = agent.vectorize(state, config)
    import asyncio
    state = asyncio.run(agent.avectorize_multi_vector_retrieve(state, config))
    state["messages"].append(HumanMessage(content="이 청약 공고문의 보증기간이 언제야?"))

    # 동기 스트림 처리(stream_mode="values")
    for chunk in agent.workflow.stream(state, config, stream_mode="values"):
        # chunk 는 dictionary 형태(key: State 의 key, value: State 의 value)
        for state_key, state_value in chunk.items():
            if state_key == "messages":
                state_value[-1].pretty_print()

    # response = agent.workflow.invoke(state, config)
    # print(response)
