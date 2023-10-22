from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
os.environ["OPENAI_API_KEY"] = ""
app = Flask(__name__)

# Function to process the uploaded PDF
def process_pdf(uploaded_pdf):
    pdfreader = PdfReader(uploaded_pdf)
    pdf_text = ''

    for page in pdfreader.pages:
        content = page.extract_text()
        if content:
            pdf_text += content

    # Split the PDF text into chunks for processing
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(pdf_text)

    # Perform embeddings
    embeddings = OpenAIEmbeddings()

    # Create the document search
    document_search = FAISS.from_texts(texts, embedding=embeddings)


@app.route('/upload', methods=['POST'])
def upload_pdf():
    global document_search
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided"})

    uploaded_pdf = request.files['pdf']

    if uploaded_pdf.filename == '':
        return jsonify({"error": "No selected file"})

    # Process the uploaded PDF
    document_search=process_pdf(uploaded_pdf)

    return jsonify({"message": "PDF processed successfully"})

@app.route('/search', methods=['GET'])
def search():
    global document_search
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Query is missing"})

    # Replace 'document_search' with your actual document search object
    # You should have this object available after processing the PDF

    # Perform a search using the query
    search_results = document_search.similarity_search(query)

    # Create a list to store the search results
    results = []

    # Iterate through the search results and extract relevant information
    for result in search_results:
        # Customize this part to extract the information you need
        result_info = {
            "page_number": result.page_number,  # Example: Page number where the result was found
            "text": result.text,  # Example: Text associated with the result
            # Add more relevant information as needed
        }
        results.append(result_info)

    # Return the search results as JSON
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run()
