"""Streamlit application for RFP document management and Q&A."""

import streamlit as st
import json
import os
from utils import (
    load_documents, 
    save_documents, 
    show_document_summary, 
    get_next_id,
    extract_rfp_info,
    get_client,
    get_completion,
    STORAGE_FILE
)

# Page configuration
st.set_page_config(
    page_title="RFP Document Manager",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "documents" not in st.session_state:
    st.session_state.documents = load_documents()

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# Title
st.title("📄 RFP Document Manager")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Document Management")
    
    # Upload RFP
    st.subheader("Upload RFP")
    uploaded_file = st.file_uploader(
        "Upload a .txt file containing RFP information",
        type=["txt"],
        help="Upload a text file with RFP details"
    )
    
    # Process uploaded file
    if uploaded_file is not None:
        # Create a unique identifier for the file
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        # Only process if not already processed
        if file_id not in st.session_state.processed_files:
            try:
                # Read the file content
                text_content = uploaded_file.read().decode("utf-8")
                
                # Extract RFP information using OpenAI
                with st.spinner("Extracting RFP information..."):
                    client = get_client()
                    rfp_doc = extract_rfp_info(text_content, client)
                    
                    # Assign ID
                    rfp_doc.id = get_next_id(st.session_state.documents)
                    
                    # Add to documents list
                    st.session_state.documents.append(rfp_doc)
                    
                    # Save to file
                    save_documents(st.session_state.documents)
                    
                    # Mark file as processed
                    st.session_state.processed_files.add(file_id)
                    
                st.success(f"✅ Successfully extracted and saved: {rfp_doc.title}")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
        else:
            st.info(f"📄 File '{uploaded_file.name}' already processed.")
    
    st.markdown("---")
    
    # Control buttons
    st.subheader("Actions")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button("🗑️ Clear Documents", use_container_width=True):
        st.session_state.documents = []
        st.session_state.processed_files = set()
        # Delete the JSON file if it exists
        if os.path.exists(STORAGE_FILE):
            os.remove(STORAGE_FILE)
        st.rerun()
    
    st.markdown("---")
    
    # Display stored documents
    st.subheader("Stored Documents")
    if st.session_state.documents:
        for doc in st.session_state.documents:
            with st.expander(f"📄 {doc.title} (ID: {doc.id})"):
                st.markdown(show_document_summary(doc))
    else:
        st.info("No documents uploaded yet.")

# Main area - Chat interface
st.header("Chat with RFP Assistant")

# Display chat messages
chat_container = st.container()
with chat_container:
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("👋 Upload an RFP document and start asking questions!")

# Chat input
user_input = st.chat_input("Ask a question about the RFP documents...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Build document context (all documents as JSON)
    docs_context = json.dumps(
        [doc.model_dump() for doc in st.session_state.documents],
        indent=2,
        ensure_ascii=False
    )
    
    # Get assistant response
    try:
        with st.spinner("Thinking..."):
            client = get_client()
            assistant_response = get_completion(
                st.session_state.chat_history,
                docs_context,
                client
            )
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": assistant_response
        })
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"Sorry, I encountered an error: {str(e)}"
        })
    
    # Rerun to display new messages
    st.rerun()
