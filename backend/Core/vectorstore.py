import pymupdf
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Load PDF
def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# Extract tables (Example using Pandas for structured tables)
def extract_table_rows_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    table_rows = []

    for page in doc:
        tables = page.find_tables()
        for table in tables:
            df = table.to_pandas()

            # Convert each row into a structured text chunk
            table_data = []
            for _, row in df.iterrows():
                row_text = " | ".join(f"{col}: {str(value)}" for col, value in row.items())
                table_data.append(row_text)

            # Create a document for each chunk
            table_rows.append(Document(page_content="\n\n".join(table_data)))

    return table_rows
def initializeVectorStore(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    tables_data = extract_table_rows_from_pdf(pdf_path)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(raw_text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    merged_doc = docs + tables_data
    vectorstore = FAISS.from_documents(merged_doc, embedding_model)
    # Save the vector store
    vectorstore.save_local("regulatory_db")
    return vectorstore

def getVectorStore(dbfolder):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(dbfolder, embedding_model, allow_dangerous_deserialization = True)