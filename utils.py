"""Utility functions for RFP document management."""

import json
import os
from typing import List
from models import RFPDocument
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default JSON file path for storing documents
STORAGE_FILE = "rfp_documents.json"


def load_documents() -> List[RFPDocument]:
    """
    Load RFP documents from JSON file.
    
    Returns:
        List of RFPDocument instances. Returns empty list if file doesn't exist.
    """
    if not os.path.exists(STORAGE_FILE):
        return []
    
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [RFPDocument(**doc) for doc in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_documents(documents: List[RFPDocument]) -> None:
    """
    Save RFP documents to JSON file with pretty formatting.
    
    Args:
        documents: List of RFPDocument instances to save
    """
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        # Convert Pydantic models to dictionaries
        data = [doc.model_dump() for doc in documents]
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_next_id(documents: List[RFPDocument]) -> int:
    """
    Generate the next auto-incrementing ID for a new document.
    
    Args:
        documents: List of existing RFPDocument instances
        
    Returns:
        Next available ID (1 if no documents exist, otherwise max_id + 1)
    """
    if not documents:
        return 1
    
    max_id = max((doc.id for doc in documents if doc.id is not None), default=0)
    return max_id + 1


def show_document_summary(doc: RFPDocument) -> str:
    """
    Generate a Markdown summary snippet for a single RFP document.
    
    Args:
        doc: RFPDocument instance to summarize
        
    Returns:
        Markdown-formatted string summarizing the document
    """
    summary = f"### {doc.title}\n\n"
    summary += f"**Company:** {doc.company}\n\n"
    
    if doc.description:
        summary += f"**Description:** {doc.description}\n\n"
    
    if doc.requirements:
        summary += f"**Requirements:** {doc.requirements}\n\n"
    
    if doc.contact:
        summary += f"**Contact:** {doc.contact}\n\n"
    
    if doc.deadline:
        summary += f"**Deadline:** {doc.deadline}\n\n"
    
    if doc.budget:
        summary += f"**Budget:** {doc.budget}\n\n"
    
    return summary


def show_document_table(docs: List[RFPDocument]) -> str:
    """
    Generate a Markdown table displaying multiple RFP documents.
    
    Args:
        docs: List of RFPDocument instances
        
    Returns:
        Markdown-formatted table with columns: ID | Title | Company | Deadline
    """
    if not docs:
        return "No documents available."
    
    # Table header
    table = "| ID | Title | Company | Deadline |\n"
    table += "|---|---|---|---|\n"
    
    # Table rows
    for doc in docs:
        doc_id = doc.id if doc.id is not None else "N/A"
        title = doc.title if doc.title else "N/A"
        company = doc.company if doc.company else "N/A"
        deadline = doc.deadline if doc.deadline else "N/A"
        
        table += f"| {doc_id} | {title} | {company} | {deadline} |\n"
    
    return table


def get_client() -> AzureOpenAI:
    """
    Initialize and return an Azure OpenAI client using environment variables.
    
    Expected environment variables:
        AZURE_OPENAI_API_KEY: Azure OpenAI API key
        AZURE_OPENAI_ENDPOINT: Azure OpenAI endpoint URL
        AZURE_OPENAI_API_VERSION: API version (e.g., '2024-02-15-preview')
        
    Returns:
        Configured AzureOpenAI client instance
    """
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


def extract_rfp_info(text: str, client: AzureOpenAI) -> RFPDocument:
    """
    Extract structured RFP information from unstructured text using Azure OpenAI.
    
    Uses OpenAI's structured outputs feature to ensure JSON response matches
    the RFPDocument schema.
    
    Args:
        text: Raw text content of the RFP document
        client: Configured AzureOpenAI client instance
        
    Returns:
        Validated RFPDocument instance with extracted information
    """
    # System prompt for extraction
    system_prompt = """You are an expert at extracting structured information from RFP documents.
Extract the following fields from the provided text:
- title: The title or name of the RFP
- company: The company or organization issuing the RFP
- description: A brief description of the project or service requested
- requirements: Key requirements or specifications
- contact: Contact information (email, phone, or person name)
- deadline: Submission deadline date
- budget: Budget or cost information

If any field is not found in the text, leave it as null. Extract information accurately."""

    # Call OpenAI with structured output
    model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_MODEL", "gpt-4")
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        response_format=RFPDocument
    )
    
    # Extract and validate the response
    rfp_data = completion.choices[0].message.parsed
    
    return rfp_data


def get_tool_definitions() -> List[dict]:
    """
    Return JSON schema definitions for function calling tools.
    
    Defines two tools that can be called by the assistant:
    - show_document_summary: Display detailed summary of specific documents by ID
    - show_document_table: Display a table of documents by ID
    
    Returns:
        List of tool definition dictionaries following OpenAI function calling schema
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "show_document_summary",
                "description": "Display a detailed Markdown summary of one or more RFP documents by their IDs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "Array of document IDs to display summaries for"
                        }
                    },
                    "required": ["ids"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "show_document_table",
                "description": "Display a Markdown table showing multiple RFP documents with columns: ID, Title, Company, Deadline",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "Array of document IDs to include in the table. If empty, show all documents."
                        }
                    },
                    "required": ["ids"],
                    "additionalProperties": False
                }
            }
        }
    ]


def get_completion(messages: List[dict], docs_context: str, client: AzureOpenAI) -> str:
    """
    Get chat completion with tool-calling support.
    
    Prepends document context to messages, calls OpenAI with tools enabled,
    and handles tool calls by executing the corresponding functions.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        docs_context: Context string containing all document information (JSON or Markdown)
        client: Configured AzureOpenAI client instance
        
    Returns:
        Assistant's response or tool execution result as a string
    """
    # Prepend system message with document context
    system_message = {
        "role": "system",
        "content": f"""You are a helpful assistant for answering questions about RFP documents.
You have access to the following RFP documents:

{docs_context}

Use the provided tools to show document summaries or tables when requested.
Answer questions accurately based on the document information provided."""
    }
    
    full_messages = [system_message] + messages
    
    # Get completion with tool calling enabled
    model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_MODEL", "gpt-4")
    response = client.chat.completions.create(
        model=model_name,
        messages=full_messages,
        tools=get_tool_definitions(),
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    
    # Check if assistant wants to call a tool
    if assistant_message.tool_calls:
        tool_call = assistant_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # Load documents for tool execution
        documents = load_documents()
        
        # Execute the requested tool
        if function_name == "show_document_summary":
            ids = function_args.get("ids", [])
            result = ""
            for doc_id in ids:
                doc = next((d for d in documents if d.id == doc_id), None)
                if doc:
                    result += show_document_summary(doc) + "\n---\n\n"
                else:
                    result += f"Document with ID {doc_id} not found.\n\n"
            return result.strip()
        
        elif function_name == "show_document_table":
            ids = function_args.get("ids", [])
            if ids:
                filtered_docs = [d for d in documents if d.id in ids]
            else:
                filtered_docs = documents
            return show_document_table(filtered_docs)
    
    # Return plain text response if no tool call
    return assistant_message.content or "No response generated."
