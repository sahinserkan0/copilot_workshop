1. Set up dependencies
Prompt to agent #1
“Using the content of requirements.txt setup a working python environment (.venv), based on these dependencies in the local workspace folder.”

Outcome: A virtual environment with all necessary packages installed.

2. Define the data models
Prompt #2
“Create models.py with two Pydantic v2 models:
RFPDocument (fields: id:int|None, title:str, company:str, plus optional description, requirements, contact, deadline, budget) and
ChatMessage (role, content).
Add type hints and docstrings.”

Outcome: validated data structures.

3. Local storage helpers
Prompt #3
“In utils.py write functions to
• load a rfp_documents.json file into a list[RFPDocument] (create an empty list if it doesn’t exist)
• save the list back (pretty-printed JSON)
• return the next auto-incrementing id.”

Outcome: persistent storage layer.

4. Markdown renderers
Prompt #4
“Extend utils.py with two pure-Python helpers:
show_document_summary(doc:RFPDocument) -> str returns a Markdown snippet summarising one document.
show_document_table(docs:list[RFPDocument]) -> str returns a Markdown table with columns ID | Title | Company | Deadline.”

Outcome: reusable formatting utilities.

5. Azure OpenAI client wrapper
Prompt #5
“Still in utils.py, add a get_client() function that returns an openai.AzureOpenAI instance initialised from AZURE_OPENAI_* env-vars. Keep it separate so we can import it elsewhere.”

Outcome: single source of truth for the client.

6. RFP information extractor
Prompt #6
“Implement extract_rfp_info(text:str, client) -> RFPDocument.
• Build an extraction system-prompt that asks for JSON with the RFP fields.
• Call client.chat.completions.create(...).
• Validate with RFPDocument.model_validate and return the model.

Use the schema utilized in https://platform.openai.com/docs/guides/structured-outputs for structuring the code.”

Outcome: automatic structured extraction.

7. Function-calling schema list
Prompt #7
“Add get_tool_definitions() -> list[dict] to utils.py.
Include JSON schemas for two tools:

show_document_summary (param: ids: array<int>)

show_document_table (param: ids: array<int>)
Schema must follow https://platform.openai.com/docs/guides/function-calling.”

Outcome: ready for tool-calling.

8. Chat completion orchestrator
Prompt #8
“Write get_completion(messages:list[dict], docs_context:str, client) in utils.py.
• Prepend a system message containing docs_context (JSON or Markdown).
• Pass messages, the tool list from get_tool_definitions, and tool_choice='auto' to the client.
• If the response contains a tool call, parse the arguments and call the corresponding Python function, then return the formatted result.
• Otherwise return the assistant’s plain content.”

Outcome: central brain for QA / tool calls.

9. Streamlit scaffold
Prompt #9
“In app.py set up a minimal Streamlit page: title, sidebar with ‘Upload RFP’, ‘Clear chat’, ‘Clear docs’. Initialise st.session_state for chat_history and documents (loaded via utils). Show a placeholder chat area.”

Outcome: running but empty UI.

Run streamlit run app.py → verify.

10. File upload → extract → store
Prompt #10
“Extend app.py: when a user uploads a .txt file:
• Read the text.
• Call extract_rfp_info.
• Append the model to the documents list and persist.
• Rerender the sidebar list using show_document_summary.
Use st.success to confirm.”

Outcome: documents flow into storage.

11. Chat interface loop
Prompt #11
“Add a text input at the bottom for user queries.
When sent:
• Append {role:'user', content:prompt} to session chat.
• Build docs_context = a concatenation of all stored docs in JSON.
• Call get_completion.
• Append the assistant’s reply (or tool output) to chat.
• Streamlit-print the conversation.”

Outcome: basic Q&A across all RFPs.

12. Clear-state controls
Prompt #12
“Wire the sidebar buttons:
• ‘Clear chat’ → empty session_state.chat_history.
• ‘Clear docs’ → delete JSON file and reload empty list.”

Outcome: housekeeping finished.



## How to use this recipe
Each prompt is intentionally narrow; the agent will generate only the code you need for that increment.

Between steps you should commit, run, and observe results (“vibe coding” in action).