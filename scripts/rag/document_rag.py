from scripts.utils import RAG


def main():
    print(f"Starting {main.__name__}")
    documents = ["../../data/audio/mp3/Simone Veil  son discours historique en faveur de lIVG.mp3"]

    RAG.rag(media_input=documents)


if __name__ == '__main__':
    main()
