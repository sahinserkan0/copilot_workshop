## Developer Workshop Instructions

1. **Setup the Project:**
    - Download the files from the Teams Group "File" section
    - Install "Python Debugger" and "Python" extensions in Visual Studio Code for debugging support. Use Python Version between 3.11 and 3.13, but not 3.14.
    - Use Visual Studio Code or your preferred IDE to open the project and initialize a virtual environment. Your integrated assistant (GitHub Copilot, Claude, or Cursor) will help you set up the environment.
    - Alternative: Install the required dependencies using `pip install -r requirements.txt`.
    - The existing **.env** file in the project folder contains the necessary environment variables for connecting to the Azure OpenAI API (a version of GPT-4o). Ensure that you are using the AzureOpenAI Client definition as provided in the master prompt.
    - If you want to use debugging, you can use the launch.json file provided in the .vscode folder to run the application in debug mode.

2. **Implement the Functionality:**
   - Use the prompting strategy, found in prompting-strategy.md, as a guide to structure your project and implement the required functionality. Alternatively, you can try to create the application using your own prompting strategy. Just make sure you cover all the necessary components, as illustrated in the screenshots in the presentation.
     - Let GitHub Copilot or your chosen assistant generate boilerplate code or even complete files based on these instructions. 
     - Ideally, you should be able to use Copilot Agent mode to guide you through the implementation process and provide suggestions for each step. 
     - **It is possible to solve this assignment without writing a single line of code yourself. In fact, this is the goal of this entire exercise.** 
     - Try to prompt the application into existence, one prompt at a time.
   - The main components to implement are:
     - The Streamlit app should load, display a sidebar with controls resetting the chat dialog, uploaded files and accept file uploads. In the main frame a regular chat interface should be displayed. **Streamlit provides easy-to-use components for these tasks.**
     - Uploaded RFP documents must be processed using Azure OpenAI and stored as valid JSON objects.
     - The chat interface should properly handle specific commands (e.g., "display a summary of document <id>", "display a table of with the properties of document <id1> and document <id2>", ...) via tool calling.
     - General queries, such as "Create a comparison of document <id1> and document <id2> and analyze their differences in the last column" or "Write an executive summary about all rfp documents that have already been processed" should be answered correctly, as well as general questions about the content of the documents.

3. **Test the Application:**
   - Run the application using `streamlit run app.py`.
   - Use the **three mock RFP documents** contained in the "genai-workshop-start" /test-data folder to verify that document extraction, storage, and display functionalities are working.
   - Test the chat interface to ensure that queries trigger your functions and produce the expected responses. 
   - (stretch-goal: test your custom document data animation or analysis functionality).

5. **Function Calling reference info**
   - You can find details on how function calling works and which syntax to use here: https://platform.openai.com/docs/guides/function-calling; however, the master prompt already contains the necessary information to implement the function calling schema.
