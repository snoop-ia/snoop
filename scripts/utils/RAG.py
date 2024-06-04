from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from scripts.utils import vector_store as vs

from typing import List, Any

import os.path
import shutil
import dotenv

dotenv.load_dotenv()

LLM_MODEL = os.getenv('LLM_MODEL')


def rag(media_input: Any):
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def display_answer(r):
        print(f"Question: {r['question']}\n")
        print(f"Answer: {r['answer']}\n")
        print(f"Sources: {r['context']}\n")
        for i, doc in enumerate(r['context'], 1):
            print(f"  {i}. {doc.metadata['source']}")

    vector_store = vs.get_vector_store(audios=media_input)

    retriever = vector_store[0].as_retriever()

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

    while True:
        query = input("Ask a question: ")
        if query == "exit":
            break

        result = rag_chain_with_source.invoke(query)
        display_answer(result)


def main():
    print(f"Starting {main.__name__}")

    # audio_files = [
    #     "../../data/audio/mp3/Comment commencer un discours  Ne plus dire bonjour mais captiver laudience dès votre arrivée.mp3",
    #     "../../data/audio/mp3/Emmanuel Macron  Nous sommes en guerre contre le coronavirus - Covid-19.mp3",
    #     "../../data/audio/mp3/Molieres  une cérémonie forte en messages politiques.mp3"
    # ]

    query = "Can you tell me what are the key points of the video?"

    rag(query=query, media_input=["https://www.youtube.com/watch?v=Mut_u40Sqz4"])


if __name__ == '__main__':
    main()
