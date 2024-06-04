from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from scripts.utils.loaders import load_youtube_videos, load_audio

from typing import List, Tuple

import os.path
import shutil
import dotenv

dotenv.load_dotenv()

CHROMA_PATH = os.getenv('CHROMA_PATH')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(documents)
    print(f"Number of chunks: {len(chunks)}, for {len(documents)} documents")
    print(f"Split documents done !")
    return chunks


def get_vector_store(**kwargs) -> Tuple[Chroma, List[Document]]:
    documents = []
    if 'audios' in kwargs:
        audios = kwargs['audios']
        documents = load_audio(audios)
    elif 'urls' in kwargs:
        urls = kwargs['urls']
        documents = load_youtube_videos(urls)

    elif 'transcriptions' in kwargs:
        documents = kwargs['documents']
        """TODO: Implement this part of the code"""

    else:
        raise ValueError("No audios or urls provided")

    documents = split_documents(documents)
    vector_store = Chroma.from_documents(documents=documents,
                                         embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))
    return vector_store, documents


def save_to_chroma(chunks: List[Document], local_save: bool = False) -> None:
    print(f"Saving {len(chunks)} documents to ChromaDB at {os.path.basename(CHROMA_PATH)}")
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    chroma = Chroma.from_documents(documents=chunks,
                                   embedding=OpenAIEmbeddings(),
                                   persist_directory=CHROMA_PATH)
    chroma.persist()
    print(f"Saved {len(chunks)} documents to ChromaDB at {CHROMA_PATH}")
    print(f"Save to Chroma done !")


def generate_vector_db(urls: List[str]) -> None:
    documents = load_youtube_videos(urls)
    chunks = split_documents(documents)
    save_to_chroma(chunks)


def main():
    print(f"Starting {main.__name__}")
    urls = [
        "https://www.youtube.com/watch?v=FgzM3zpZ55o",
        "https://www.youtube.com/watch?v=E3f2Camj0Is",
        "https://www.youtube.com/watch?v=dRIhrn8cc9w",
    ]

    generate_data_for_rag(urls)
    print(f"Finished {main.__name__}")


if __name__ == '__main__':
    main()
