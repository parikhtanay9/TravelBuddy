import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import requests
from config import GOOGLE_MAPS_API_KEY, PROJECT_ID, LOCATION, MODEL_ENDPOINT

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Configure the generation settings
config = generative_models.GenerationConfig(temperature=0.4)

# Load the model with the specified configuration
model = GenerativeModel(MODEL_ENDPOINT, generation_config=config)

# Start a chat session
chat = model.start_chat()

# Helper function to get nearby places using Google Maps API
def get_nearby_places(lat, lon, radius, place_type):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius={radius}&type={place_type}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    places = response.json().get('results', [])
    return places

# Helper function to display and send Streamlit messages
def llm_function(chat: ChatSession, query, user_name):
    personalized_query = f"{query} (User name: {user_name})"
    response = chat.send_message(personalized_query)
    response_text = response.candidates[0].content.parts[0].text
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

# Initialize the chat hisCS\\ory in the Streamlit session state if it does not already exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add initial prompt if message history is empty
if len(st.session_state.messages) == 0 and st.session_state.user_name:
    initial_prompt = f"Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive and greet the user {st.session_state.user_name}."
    llm_function(chat, initial_prompt, st.session_state.user_name)

# Display and load chat history
for index, message in enumerate(st.session_state.messages):
    st.write(f"Message {index + 1}: {message}")

# Capture user input
query = st.text_input("Enter your query for Gemini Explorer")
if st.button("Submit"):
    if query and st.session_state.user_name:
        # Process the user's query using the llm_function
        llm_function(chat, query, st.session_state.user_name)

# Capture location and radius from the user
lat = st.number_input("Enter your latitude", format="%.6f")
lon = st.number_input("Enter your longitude", format="%.6f")
radius = st.number_input("Enter the search radius in meters", min_value=1, step=1)
place_type = st.selectbox("Select the type of place", ["tourist_attraction", "restaurant", "gas_station"])

if st.button("Find Places"):
    if lat and lon and radius and place_type:
        places = get_nearby_places(lat, lon, radius, place_type)
        if places:
            st.write(f"Found the following places within {radius} meters:")
            for place in places:
                st.write(f"{place['name']} ({place['vicinity']})")
        else:
            st.write("No places found nearby.")

# Debugging: Print the entire session state
print(st.session_state)
