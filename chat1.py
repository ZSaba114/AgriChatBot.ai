# chat1.py
import requests
import PyPDF2
from itertools import chain
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# ============================
# Fetch content from a website
# ============================
def fetch_website_content(url):
    """
    Récupère le contenu HTML d'une page web.
    Args:
        url (str): URL du site web
    Returns:
        str: Contenu HTML brut
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

# ============================
# Extract text from a PDF file
# ============================
def extract_pdf_text(pdf_file):
    """
    Extrait le texte d'un fichier PDF.
    Args:
        pdf_file (str): chemin vers le PDF
    Returns:
        str: texte extrait
    """
    text = ""
    try:
        with open(pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[page_num].extract_text()
                if page_text:
                    text += page_text
    except FileNotFoundError:
        print(f"PDF file not found: {pdf_file}")
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
    return text

# ============================
# Split text into smaller chunks
# ============================
def split_text(text, chunk_size=500, chunk_overlap=100):
    """
    Divise le texte en petits segments pour embeddings.
    Args:
        text (str): texte à diviser
        chunk_size (int): taille de chaque chunk
        chunk_overlap (int): chevauchement entre chunks
    Returns:
        List[str]: liste de segments de texte
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks

# ============================
# Initialize embeddings and vector store
# ============================
def initialize_vector_store(contents):
    """
    Initialise le vector store Chroma avec les embeddings.
    Args:
        contents (List[str]): liste de contenus textuels
    Returns:
        Chroma: objet vector store prêt pour RetrievalQA
    """
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # Découpe tous les contenus en chunks
    web_chunks = list(chain.from_iterable(split_text(content) for content in contents))
    # Crée le vector store
    db = Chroma.from_texts(web_chunks, embedding_function)
    return db
