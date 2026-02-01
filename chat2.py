# chat2.py
from langchain_together import Together
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ============================
# Initialize the language model
# ============================
llm = Together(
    model="meta-llama/Llama-2-70b-chat-hf",
    max_tokens=512,
    temperature=0.1,
    top_k=1,
    # Remplacez par votre clé API Together
    together_api_key="YOUR_Together_API_KEY"
)

# ============================
# Setup the RetrievalQA chain
# ============================
def setup_retrieval_qa(db):
    """
    Configure la chaîne RetrievalQA pour AgriChatBot.
    
    Args:
        db: Vector store Chroma initialisé avec le contenu agricole
    
    Returns:
        chain: objet RetrievalQA prêt à répondre aux questions
    """
    # Récupérateur avec seuil de similarité
    retriever = db.as_retriever(similarity_score_threshold=0.6)

    # Prompt template personnalisé
    prompt_template = """ 
Your name is AgriChatBot. Please answer questions related to Agriculture.
Explain in simple words, in less than 100 words. 
If you don't know the answer, simply respond with 'Don't know.'

CONTEXT: {context}
QUESTION: {question}
"""

    PROMPT = PromptTemplate(
        template=f"[INST] {prompt_template} [/INST]",
        input_variables=["context", "question"]
    )

    # Initialiser la chaîne RetrievalQA
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        input_key='query',
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
        verbose=True
    )

    return chain
