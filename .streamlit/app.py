import streamlit as st
import os
import pandas as pd
from PIL import Image
import tempfile
import re
import base64
from streamlit.components.v1 import html
import io

# Import the required functions
from jiu_jitsu_functions import (
    generate_grappling_plan,
    analyse_grappling_match,
    generate_flow_chart,
    gracie_talk,
    generate_mermaid,
    display_graph,
    next_move,
    get_attributes
)

from genai import GenAI
from movieai import MovieAI

# Set page configuration
st.set_page_config(page_title="Jiu-Jitsu Genie", layout="wide")

# Custom CSS for black and white theme
st.markdown("""
<style>
    .main {
        background-color: white;
        color: black;
    }
    .stButton button {
        background-color: black;
        color: white;
        border-radius: 5px;
    }
    .stTextInput, .stTextArea, .stSelectbox {
        border: 1px solid black;
    }
    .stSidebar {
        background-color: #f0f0f0;
    }
    .highlight {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .error {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = []
if 'current_flowchart' not in st.session_state:
    st.session_state.current_flowchart = None
if 'current_video' not in st.session_state:
    st.session_state.current_video = None
if 'current_attributes' not in st.session_state:
    st.session_state.current_attributes = ""

# Load masters list
def load_masters():
    try:
        with open("masters.txt", "r") as file:
            masters = [line.strip() for line in file if line.strip()]
        return masters
    except FileNotFoundError:
        return ["John Danaher", "Rickson Gracie", "Roger Gracie", "Marcelo Garcia", "Gordon Ryan", 
                "Kyra Gracie", "Helio Gracie", "Carlos Gracie", "Eddie Bravo", "Andre Galvao", 
                "Buchecha", "Keenan Cornelius", "Bernardo Faria", "Renzo Gracie", "Jean Jacques Machado"]

# Function to render mermaid chart
def render_mermaid(chart):
    html_content = display_graph(chart)
    return html(html_content, height=600)

# Sidebar for navigation
st.sidebar.title("Jiu-Jitsu Genie")
app_function = st.sidebar.selectbox(
    "Choose a function",
    ["Position Image Recommendations", "Master Talk", "FLOW Chart Generator", "Video Match Analysis"]
)

# Initialize OpenAI API key - In a real application, use better security practices
if 'OPENAI_API_KEY' not in os.environ:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if openai_api_key:
        os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
        st.sidebar.warning("Please enter your OpenAI API Key")

# Function: Position Image Recommendations
if app_function == "Position Image Recommendations":
    st.title("Position Image Recommendations")
    
    # Image upload
    uploaded_file = st.file_uploader("Upload an image of a jiu-jitsu position", type=['jpg', 'jpeg', 'png'])
    image_location = None
    
    # Display the uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300)
        
        # Save the image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image_location = tmp_file.name
            image.save(image_location)
        
        # Update session state
        st.session_state.current_image = image_location
    
    # User inputs
    position_variable = st.text_input("Enter the jiu-jitsu position")
    isMMA = st.selectbox("Ruleset is MMA?", ["True", "False"]) == "True"
    keywords = st.text_area("Enter your ideas or keywords", height=100)
    
    # Process button
    if st.button("Generate Recommendations"):
        if not image_location or not position_variable or not keywords:
            st.error("Please fill in all fields and upload an image")
        else:
            with st.spinner("Analyzing position and generating recommendations..."):
                try:
                    # Get attributes
                    attributes = get_attributes(image_location, position_variable)
                    st.session_state.current_attributes = attributes
                    
                    # Update keywords with attributes
                    enhanced_keywords = keywords + " " + attributes
                    
                    # Generate recommendations
                    recommendations = generate_grappling_plan(image_location, position_variable, isMMA, enhanced_keywords)
                    
                    # Display recommendations in a bounded text box
                    st.markdown("### Recommendations")
                    st.markdown(f'<div class="highlight">{recommendations}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Function: Master Talk
elif app_function == "Master Talk":
    st.title("Master Talk")
    
    # Load masters list
    masters = load_masters()
    
    # Master selection dropdown
    master_info = st.selectbox("Select a Jiu-Jitsu Master", masters)
    
    # Initialize chat if needed
    if len(st.session_state.current_chat) == 0:
        instructions = f"You are the jiu-jitsu master {master_info}. Have a conversation to me as this master and provide me troubleshooting help on my jiu-jitsu based on your fundamental principles of jiujitsu and notable successes."
        prompt = "Start a conversation to help me with my jiu-jitsu"
        
        # Initialize GenAI
        if 'OPENAI_API_KEY' in os.environ:
            genai = GenAI(os.environ.get("OPENAI_API_KEY"))
            initial_response = genai.generate_text(prompt, instructions)
            
            # Update chat history
            st.session_state.current_chat = [
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": initial_response}
            ]
    
    # Display chat history
    st.markdown("### Conversation")
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.current_chat:
            if message["role"] != "system":
                role = "You" if message["role"] == "user" else f"Master {master_info}"
                st.markdown(f"**{role}**: {message['content']}")
    
    # Chat input
    next_comment = st.text_input("Your message:")
    
    if st.button("Send") and next_comment:
        if 'OPENAI_API_KEY' in os.environ:
            genai = GenAI(os.environ.get("OPENAI_API_KEY"))
            instructions = f"You are the jiu-jitsu master {master_info}. Have a conversation to me as this master and provide me troubleshooting help on my jiu-jitsu based on your fundamental principles of jiujitsu and notable successes."
            
            response = genai.generate_chat_response(
                st.session_state.current_chat,
                next_comment,
                instructions
            )
            
            # Update chat history
            st.session_state.current_chat.append({"role": "user", "content": next_comment})
            st.session_state.current_chat.append({"role": "assistant", "content": response})
            
            # Rerun to update displayed conversation
            st.experimental_rerun()
    
    # Button to switch to FLOW Chart Generator
    if st.button("Generate FLOW"):
        app_function = "FLOW Chart Generator"
        st.experimental_rerun()

# Function: FLOW Chart Generator
elif app_function == "FLOW Chart Generator":
    st.title("FLOW Chart Generator")
    
    # User inputs
    position_variable = st.text_input("Starting Position")
    rules = st.selectbox("Rules", ["Unified MMA", "IBJJF"])
    isMMA = rules == "Unified MMA"
    ideas = st.text_area("Ideas", height=100)
    
    # Process attributes if an image has been uploaded
    attributes = ""
    if st.session_state.current_image and position_variable:
        try:
            attributes = get_attributes(st.session_state.current_image, position_variable)
            st.session_state.current_attributes = attributes
            st.success("Position attributes analyzed!")
        except Exception as e:
            st.warning(f"Could not analyze position attributes: {str(e)}")
    
    # Generate flow chart button
    if st.button("Generate Flow Chart"):
        if not position_variable:
            st.error("Please enter a starting position")
        else:
            with st.spinner("Generating flow chart..."):
                try:
                    # Generate flow chart
                    flow_chart = generate_flow_chart(
                        attributes if attributes else st.session_state.current_attributes,
                        position_variable,
                        isMMA,
                        ideas
                    )
                    
                    # Update session state
                    st.session_state.current_flowchart = flow_chart
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    # Display flow chart if available
    if st.session_state.current_flowchart:
        st.markdown("### Flow Chart")
        render_mermaid(st.session_state.current_flowchart)
        
        # Next move selection
        chosen_next = st.text_input("Choose a next move")
        
        if st.button("Flow") and chosen_next:
            # Check if the move exists in the flowchart
            found = False
            if st.session_state.current_flowchart:
                # Simple check if the node or line exists in the flowchart
                found = chosen_next in st.session_state.current_flowchart
            
            if not found:
                st.error("Osu! That move is not in the current flow chart. Try another move.")
            else:
                with st.spinner("Generating next flow..."):
                    try:
                        # Generate next flow chart
                        next_flowchart = next_move(
                            st.session_state.current_flowchart,
                            chosen_next,
                            st.session_state.current_attributes,
                            isMMA,
                            ideas
                        )
                        
                        # Update session state
                        st.session_state.current_flowchart = next_flowchart
                        
                        # Force a rerun to update the displayed chart
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

# Function: Video Match Analysis
elif app_function == "Video Match Analysis":
    st.title("Video Match Analysis")
    
    # Video upload
    uploaded_file = st.file_uploader("Upload a video of a jiu-jitsu match", type=['mp4', 'mov', 'avi'])
    
    # Master selection for video analysis
    masters = load_masters()
    selected_master = st.selectbox("Select a Jiu-Jitsu Master for analysis", masters, index=0)
    
    if uploaded_file is not None:
        # Save the video temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name
        
        # Update session state
        st.session_state.current_video = video_path
        
        # Display the video
        st.video(video_path)
        
        # Analyze button
        if st.button("Analyze Video"):
            with st.spinner("Analyzing video..."):
                try:
                    # Initialize MovieAI
                    if 'OPENAI_API_KEY' in os.environ:
                        movie_ai = MovieAI(os.environ.get("OPENAI_API_KEY"))
                        
                        # If no image has been uploaded, extract a frame from the video
                        if not st.session_state.current_image:
                            # Extract frames
                            base64Frames, nframes, fps = movie_ai.extract_frames(video_path, max_samples=1)
                            
                            if base64Frames:
                                # Save the frame as an image
                                image_data = base64.b64decode(base64Frames[0])
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as img_file:
                                    img_file.write(image_data)
                                    frame_path = img_file.name
                                
                                # Update session state
                                st.session_state.current_image = frame_path
                                st.success("Extracted frame from video as current image")
                                
                                # Get attributes
                                st.session_state.current_attributes = get_attributes(frame_path, "both")
                        
                        # Extract multiple frames for analysis
                        video_length = 30  # Default assumption, could be calculated
                        num_frames = max(3, int(video_length / 3))
                        base64Frames, nframes, fps = movie_ai.extract_frames(video_path, max_samples=num_frames)
                        
                        # Create temporary image files for the frames
                        frame_paths = []
                        for i, frame in enumerate(base64Frames):
                            image_data = base64.b64decode(frame)
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as img_file:
                                img_file.write(image_data)
                                frame_paths.append(img_file.name)
                        
                        # Analyze each frame
                        analysis_results = []
                        for i, frame_path in enumerate(frame_paths):
                            instructions = f"As {selected_master}, analyze this jiu-jitsu position frame. Provide insights on technique, strategy, and potential improvements."
                            description = movie_ai.generate_image_description(frame_path, instructions)
                            analysis_results.append(f"### Frame {i+1}:\n{description}")
                        
                        # Display results
                        st.markdown("## Analysis Results")
                        for result in analysis_results:
                            st.markdown(result)
                    else:
                        st.error("OpenAI API Key is required for video analysis")
                except Exception as e:
                    st.error(f"An error occurred during video analysis: {str(e)}")