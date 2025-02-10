import os
import streamlit as st
# from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel

# Load environment variables
load_dotenv()

# Configure Gemini API
configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="AI News Generator", page_icon="📰", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main { background-color: #f4f4f9; }
        h1 { color: #1e3a8a; }
        .markdown-text-container { color: #333; }
        .css-1d391kg { background-color: #2d3748; color: white; }
        .stButton>button { background-color: #3182ce; color: white; border-radius: 5px; }
        .stButton>button:hover { background-color: #63b3ed; }
        .stTextArea>div>div>textarea { background-color: #edf2f7; border: 1px solid #cbd5e0; color: #4a5568; }
        .stSlider>div>div>input[type="range"] { background: linear-gradient(to right, #4caf50, #ff9800, #f44336); }
        .stExpander>div>div { background-color: #e2e8f0; color: #2d3748; }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 AI News Generator, powered by CrewAI and Gemini API")
st.markdown("Generate comprehensive blog posts about any topic using AI agents.")

# Sidebar
with st.sidebar:
    st.header("Content Settings")
    topic = st.text_area("Enter your topic", height=100,
                         placeholder="Enter the topic you want to generate content about...")
    st.markdown("### Advanced Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    st.markdown("---")
    generate_button = st.button("Generate Content", type="primary", use_container_width=True)

    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Enter your desired topic in the text area above
        2. Adjust the temperature if needed (higher = more creative)
        3. Click 'Generate Content' to start
        4. Wait for the AI to generate your article
        5. Download the result as a markdown file
        """)


# Function to generate content using Gemini API
def generate_content(topic):
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(f"Generate a comprehensive blog post about {topic}.")
    return response.text if response else "No content generated."


# Main content area
if generate_button:
    with st.spinner('Generating content... This may take a moment.'):
        try:
            result = generate_content(topic)
            st.markdown("### Generated Content")
            st.markdown(result)

            st.download_button(
                label="Download Content",
                data=result,
                file_name=f"{topic.lower().replace(' ', '_')}_article.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, Streamlit, and powered by Gemini API")
