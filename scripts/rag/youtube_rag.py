from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from scripts.rag import vector_store as vs

import os.path
import shutil
import dotenv

dotenv.load_dotenv()

LOCAL = os.getenv('LOCAL')
SAVE_DIR = os.getenv('SAVE_DIR')
CHROMA_PATH = os.getenv('CHROMA_PATH')
WHISPER_MODEL = os.getenv('WHISPER_MODEL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    print(f"Starting {main.__name__}")

    urls = [
        "https://www.youtube.com/watch?v=FgzM3zpZ55o",
        "https://www.youtube.com/watch?v=E3f2Camj0Is",
        "https://www.youtube.com/watch?v=dRIhrn8cc9w",
    ]

    vector_store = vs.get_vector_store(urls)

    retriever = vector_store.as_retriever()

    prompt = hub.pull("rlm/rag-prompt")

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | prompt
            | llm
            | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    result = rag_chain_with_source.invoke("Can you explain me what's the sequential decision making?")
    print(f"Question : {result['question']}")
    print(f"Answer : {result['answer']}")
    print(f"Sources : {result['context']}")


if __name__ == '__main__':
    main()
