from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain_community.document_loaders.text import TextLoader

from langchain_community.document_loaders.parsers import OpenAIWhisperParser
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParserLocal
from langchain.schema import Document

from typing import List, Tuple

import os.path
import shutil
import dotenv

dotenv.load_dotenv()

WHISPER_LOCAL = os.getenv('WHISPER_LOCAL')
SAVE_DIR = os.getenv('SAVE_DIR')
CHROMA_PATH = os.getenv('CHROMA_PATH')
WHISPER_MODEL = os.getenv('WHISPER_MODEL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def load_youtube_videos(urls: List[str]) -> List[Document]:
    if WHISPER_LOCAL == "True":
        print("Working in local mode")
        loader = GenericLoader(
            YoutubeAudioLoader(urls, SAVE_DIR),
            OpenAIWhisperParserLocal(lang_model=WHISPER_MODEL))
    else:
        print("Working in remote mode")
        loader = GenericLoader(
            YoutubeAudioLoader(urls, SAVE_DIR),
            OpenAIWhisperParser(api_key=OPENAI_API_KEY)
        )
    documents = loader.load()

    print(f"Loaded {len(documents)} documents")
    print(f"Load videos done !")
    return documents


def load_audio(audios: List[str]) -> List[Document]:
    def combine_documents(document_list: List[Document]) -> Document:
        return [doc for doc_list in document_list for doc in doc_list]

    loaders = []
    print(f"Number of audio files: {len(audios)}")
    if WHISPER_LOCAL:
        for audio in audios:
            loader = GenericLoader.from_filesystem(path=audio, parser=OpenAIWhisperParserLocal(lang_model=WHISPER_MODEL))
            loaders.append(loader)

    else:
        for audio in audios:
            loader = GenericLoader.from_filesystem(path=audio, parser=OpenAIWhisperParser(api_key=OPENAI_API_KEY))
            loaders.append(loader)

    documents = combine_documents([loader.load() for loader in loaders])
    print(f"Loaded {len(documents)} documents_loaded")
    return documents


def load_transcriptions(documents: List[str]) -> List[Document]:
    pass
