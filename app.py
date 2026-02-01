# app.py
from flask import Flask, render_template, request, jsonify
from chat1 import fetch_website_content, extract_pdf_text, initialize_vector_store
from chat2 import llm, setup_retrieval_qa

app = Flask(__name__)

# ============================
# Configuration AgriChatBot
# ============================

# Exemple de sites agricoles et fichiers PDF
urls = ["https://mospi.gov.in/4-agricultural-statistics"]  
pdf_files = ["Data/Farming Schemes.pdf", "Data/farmerbook.pdf"]

# Récupérer le contenu des sites web
website_contents = [fetch_website_content(url) for url in urls]

# Extraire le texte des fichiers PDF
pdf_texts = [extract_pdf_text(pdf_file) for pdf_file in pdf_files]

# Combiner tout le contenu
all_contents = website_contents + pdf_texts

# Initialiser le vector store
db = initialize_vector_store(all_contents)

# Configurer la chaîne RetrievalQA
chain = setup_retrieval_qa(db)

# ============================
# Routes Flask
# ============================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['messageText'].strip().lower()

    # Réponses aux questions sur l'auteur
    if query in ["who developed you?", "who created you?", "who made you?"]:
        return jsonify({"answer": "I was developed by Saba Zeibi."})
    
    # Réponse du chatbot
    response = chain(query)
    return jsonify({"answer": response['result']})

# ============================
# Lancement de l'application
# ============================

if __name__ == "__main__":
    # debug=True pour le développement local
    app.run(debug=True)
