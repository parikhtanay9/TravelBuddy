import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, ChatSession

# Set up project ID and location
project_id = "gemini-explorer-426501"  # Replace with your actual project ID
location = "us-central1"  # The location where your model is deployed

vertexai.init(project=project_id, location=location)

# Configure the generation settings
config = generative_models.GenerationConfig(
    temperature=0.4
)

# Specify the full model endpoint
model_endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/gemini-pro"

# Load the model with the specified configuration
model = GenerativeModel(
    model_endpoint,
    generation_config=config
)

# Start a chat session
chat = model.start_chat()

# Helper function to display and send Streamlit messages
def llm_function(chat: ChatSession, query, user_name):
    personalized_query = f"{query} (User name: {user_name})"
    response = chat.send_message(personalized_query)

    # Extract the response text
    response_text = response.candidates[0].content.parts[0].text

    # Debugging: Print response to console
    print(response_text)

    st.write(response_text)

    st.session_state.messages.append(response_text)

# Set the title for the Streamlit app
st.title("Gemini Explorer")

# Capture user name
user_name = st.text_input("Enter your name")
if "user_name" not in st.session_state:
    st.session_state.user_name = user_name
elif user_name:
    st.session_state.user_name = user_name  # Update the user name if it is provided again

# Initialize the chat history in the Streamlit session state if it does not already exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add initial prompt if message history is empty
if len(st.session_state.messages) == 0 and st.session_state.user_name:
    initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive and greet the user {st.session_state.user_name}."
    llm_function(chat, initial_prompt, st.session_state.user_name)

# Display and load chat history
for index, message in enumerate(st.session_state.messages):
    st.write(f"Message {index + 1}: {message}")

# Capture user input
query = st.text_input("Enter your query for Gemini Flights")
if st.button("Submit"):
    if query and st.session_state.user_name:
        # Process the user's query using the llm_function
        llm_function(chat, query, st.session_state.user_name)

# Debugging: Print the entire session state
print(st.session_state)
