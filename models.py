"""Data models for RFP document management application."""

from pydantic import BaseModel, Field
from typing import Optional


class RFPDocument(BaseModel):
    """
    Represents a Request for Proposal (RFP) document.
    
    Attributes:
        id: Unique identifier for the document (auto-assigned if None)
        title: Title of the RFP
        company: Company name issuing the RFP
        description: Optional detailed description of the RFP
        requirements: Optional list of requirements or specifications
        contact: Optional contact information
        deadline: Optional submission deadline
        budget: Optional budget information
    """
    id: Optional[int] = None
    title: str
    company: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    contact: Optional[str] = None
    deadline: Optional[str] = None
    budget: Optional[str] = None


class ChatMessage(BaseModel):
    """
    Represents a chat message in the conversation.
    
    Attributes:
        role: Role of the message sender (e.g., 'user', 'assistant', 'system')
        content: Content of the message
    """
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")
