import os
import pandas as pd
import time
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.core.rag import vector_store

DATA_FOLDER = "data"

def find_header_row(df_preview):
    """
    Scans the first 10 rows to find the likely header row.
    Looks for keywords common in your Ministry documents.
    """
    keywords = ["ITEM", "DESCRIPTION", "PARTICULARS", "UNIT COST", "RATE", "AMOUNT", "TOTAL", "QTY"]
    
    for i, row in df_preview.iterrows():
        # Convert row to string and check if it contains multiple keywords
        row_str = " ".join([str(val).upper() for val in row.values])
        matches = sum(1 for k in keywords if k in row_str)
        
        # If we find at least 2 keywords (e.g., "ITEM" and "AMOUNT"), this is the header!
        if matches >= 2:
            return i
            
    return 0 # Default to first row if nothing found

def load_excel(file_path):
    documents = []
    try:
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            # 1. Read first 15 rows just to find the header
            preview_df = pd.read_excel(xls, sheet_name=sheet_name, nrows=15, header=None)
            header_idx = find_header_row(preview_df)
            
            # 2. Read the actual data using the correct header row
            df = pd.read_excel(xls, sheet_name=sheet_name, header=header_idx)
            df = df.fillna("")
            
            print(f"     -> Sheet '{sheet_name}': Found headers at Row {header_idx + 1}")

            text_rows = []
            for index, row in df.iterrows():
                # Skip empty rows or rows that just repeat headers
                if not any(str(val).strip() for val in row.values):
                    continue
                    
                row_str = f"Source: {os.path.basename(file_path)} | Sheet: {sheet_name} | "
                # Clean format: "Item: Fuel" instead of "Unnamed: 1: Fuel"
                row_parts = []
                for col, val in row.items():
                    # clean content
                    val_str = str(val).strip()
                    if not val_str or val_str.lower() == "nan": continue
                    
                    # clean header (remove newlines in headers often found in Gov docs)
                    col_name = str(col).replace("\n", " ").strip()
                    if "Unnamed" in col_name: continue # Skip junk columns
                    
                    row_parts.append(f"{col_name}: {val_str}")
                
                if row_parts:
                    row_str += " | ".join(row_parts)
                    text_rows.append(row_str)
            
            # Group rows
            chunk_size = 10
            for i in range(0, len(text_rows), chunk_size):
                chunk = "\n".join(text_rows[i:i+chunk_size])
                documents.append(Document(page_content=chunk, metadata={"source": file_path, "sheet": sheet_name}))
                
    except Exception as e:
        print(f"⚠️ Error reading Excel {file_path}: {e}")
        
    return documents

def ingest_data():
    if not os.path.exists(DATA_FOLDER):
        print(f"❌ '{DATA_FOLDER}' folder missing.")
        return

    print(f"📂 Scanning '{DATA_FOLDER}'...")
    all_docs = []
    
    for filename in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, filename)
        
        if filename.endswith(".docx"):
            try:
                loader = Docx2txtLoader(file_path)
                all_docs.extend(loader.load())
                print(f"   - 📝 Loaded Word: {filename}")
            except: pass

        elif filename.endswith(".xlsx"):
            print(f"   - 📊 Processing Excel: {filename}")
            all_docs.extend(load_excel(file_path))

        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            all_docs.extend(loader.load())
            print(f"   - 📕 Loaded PDF: {filename}")

    if not all_docs:
        print("⚠️ No valid files found.")
        return

    print(f"🔪 Splitting {len(all_docs)} docs...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    docs = text_splitter.split_documents(all_docs)

    print(f"📦 Uploading {len(docs)} chunks to Supabase Brain...")
    
    batch_size = 10 
    for i in range(0, len(docs), batch_size):
        try:
            batch = docs[i:i+batch_size]
            vector_store.add_documents(batch)
            print(f"   - Uploaded batch {i//batch_size + 1} (Sleeping 5s...)")
            time.sleep(5) # < - Patience fix with rate limits
        except Exception as e:
            print(f"   ❌ Batch upload failed: {e}")
            time.sleep(10)
    
    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    ingest_data()