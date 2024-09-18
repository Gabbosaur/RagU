import os
import streamlit as st
import subprocess

# Define the folder where files will be saved
SAVE_FOLDER = 'data'

# Create the folder if it doesn't exist
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Path to the query_data script
POPULATE_DB_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'populate_database.py')
QUERY_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'query_data.py')


# Section 1: Drag and Drop for PDF and Markdown files
st.set_page_config(
    page_title="RagU",  # Set your custom page title
    page_icon="ragu-logo.png"  # Path to your favicon image file (can be a local path or a URL)
)

st.title("🍝 RagU")
st.subheader("Go-to app for flavorful document chats and intelligent insights")
st.sidebar.header("📤 Upload Section")
uploaded_files = st.sidebar.file_uploader("Upload PDF or Markdown files", type=['pdf', 'md'], accept_multiple_files=True)

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        # Define the save path
        save_path = os.path.join(SAVE_FOLDER, uploaded_file.name)

        # Check if file with the same name already exists
        if os.path.exists(save_path):
            st.warning(f"File '{uploaded_file.name}' already exists. It won't be uploaded.")
        else:
            # Save the file if it doesn't already exist
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"File '{uploaded_file.name}' has been saved to {SAVE_FOLDER}.")

# Function to list files in the SAVE_FOLDER directory
def list_uploaded_files():
    try:
        files = os.listdir(SAVE_FOLDER)
        if len(files) == 0:
            return None
        else:
            return files
    except Exception as e:
        st.error(f"Error listing files: {e}")
        return None

# Function to delete a file from the SAVE_FOLDER directory
def delete_file(file_name):
    file_path = os.path.join(SAVE_FOLDER, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success(f"File '{file_name}' has been deleted.")
    else:
        st.error(f"File '{file_name}' not found.")

# Inject custom CSS for compact file tiles
st.markdown(
    """
    <style>
    .file-list {
        margin-bottom: 20px;
    }
    .file-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 8px;
        margin-bottom: 4px;
        border-bottom: 1px solid #ddd;
    }
    .file-item span {
        font-size: 0.9em;
    }
    .small-button {
        font-size: 0.75em;
        padding: 2px 6px;
        background-color: #f44336;
        color: white;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Section 3: List and Delete Uploaded Files
st.sidebar.header("🛢 Uploaded Files")

files = list_uploaded_files()

with st.sidebar.form(key="delete_form"):
    if files:
        selected_file = st.selectbox("Select a file to delete", files)
        delete_button = st.form_submit_button("Delete Selected File", use_container_width=True)
        
        if delete_button:
            delete_file(selected_file)
    else:
        st.write("No uploaded files found.")

# Section 4: Run External Script
st.sidebar.header("🔄 Update Knowledge Base")

reset_option = st.sidebar.checkbox("Reset Database", value=False)

if st.sidebar.button("Update"):
    script_command = ["python3", POPULATE_DB_SCRIPT_PATH]
    if reset_option:
        script_command.append("--reset")
    
    with st.spinner('Updating database...'):
        result = subprocess.run(script_command, capture_output=True, text=True)
        st.text(result.stdout)
        if result.stderr:
            st.error(result.stderr)

# Section 2: Chatting with a model
st.subheader("Chat with the model")

# History to store the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

def chat_with_model(user_input):
    # Call the OpenAI API (or any other model) for a chat response
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=st.session_state.messages + [{"role": "user", "content": user_input}],
    #     temperature=0.7,
    # )
    pass
    
    return "Model response placeholder"

# Chat Input
user_input = st.text_input("You:", key="input")

if st.button("Send", type="primary") and user_input:
    # Construct the command with user input
    command = ["python3", QUERY_SCRIPT_PATH, user_input]
    
    # Execute the command
    with st.spinner('Running query...'):
        result = subprocess.run(command, capture_output=True, text=True)
        st.success(result.stdout)
        if result.stderr:
            st.error(result.stderr)
    
    # Optionally, store the conversation in session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": "Query executed."})

# Display chat history
# for message in st.session_state.messages:
#     if message["role"] == "user":
#         st.markdown(f"**You**: {message['content']}")
#     else:
#         st.markdown(f"**Assistant**: {message['content']}")



