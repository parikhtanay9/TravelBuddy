import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Set up project ID and location
project_id = "gemini-explorer-426501"  # Replace with your actual project ID
location = "us-central1"  # The location where your model is deployed

vertexai.init(project=project_id, location=location)

config = generative_models.GenerationConfig(
    temperature=0.4
)
# Specify the full model endpoint
model_endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/gemini-pro"


# Attempt to load the model with the correct endpoint
try:
    # Load the model with the specified configuration
    model = GenerativeModel(
        model_endpoint,
        generation_config=config
    )
    chat = model.start_chat()
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

#helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)

    st.write(response)

    st.session_state.messages.append(response)
        
# Set the title for the Streamlit app
st.title("Gemini Explorer")

# Initialize the chat history in the Streamlit session state if it does not already exist
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display and load chat history
for index, message in enumerate(st.session_state.messages):
    st.write(f"Message {index + 1}: {message}")

#captures user input
query = st.text_input("Enter your query for Gemini Flights")
if st.button("Submit"):
    if query:
        # Process the user's query using the llm_function
        llm_function(chat, query)