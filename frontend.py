import streamlit as st
import requests
import tempfile
import os

# Define the Flask API URL
API_URL = "http://127.0.0.1:5000"  # Replace with your Flask API URL

# Create a temporary directory to store uploaded files
temp_dir = tempfile.TemporaryDirectory()

st.title("PDF Search Application")

# Create a file upload widget for PDF files
uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

# Create a text input for the search query
query = st.text_input("Enter your query:")

if uploaded_pdf:
    # Display the uploaded PDF for user reference
    st.write("Uploaded PDF File:")
    st.write(uploaded_pdf)

if st.button("Upload PDF and Search"):
    if not uploaded_pdf:
        st.error("Please upload a PDF file.")
    else:
        # Upload the PDF to the Flask backend
        uploaded_pdf_path = os.path.join(temp_dir.name, uploaded_pdf.name)
        with open(uploaded_pdf_path, "wb") as pdf_file:
            pdf_file.write(uploaded_pdf.read())

        response = requests.post(f"{API_URL}/upload", files={"pdf": (uploaded_pdf.name, open(uploaded_pdf_path, "rb"))})

        if response.status_code == 200:
            st.success("PDF processed successfully")
        else:
            st.error("Error processing the PDF")

        # Perform a search using the query
        if query:
            search_response = requests.get(f"{API_URL}/search?query={query}")

            if search_response.status_code == 200:
                results = search_response.json()["results"]
                st.write("Search results:")
                for result in results:
                    # Customize the result display as needed
                    st.write(f"Page Number: {result['page_number']}")
                    st.write(f"Text: {result['text']}")
            else:
                st.error("Error searching for the query")
