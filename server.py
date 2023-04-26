import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from dotenv import load_dotenv

load_dotenv()

with open("./rules/magic-the-gathering.txt") as f:
    rules = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(rules)

embeddings = OpenAIEmbeddings()

docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": f"{i}-pl"} for i in range(len(texts))])

chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever())

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv("CLIENT_URL")}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/question', methods=['POST'])
@cross_origin()
def post_data():
    data = request.get_json()

    print(data)
    response = chain({"question": data["question"]}, return_only_outputs=True)
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run()
