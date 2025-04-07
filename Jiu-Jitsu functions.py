import os
import cv2
from genai import GenAI

def generate_grappling_plan(image_path, player_variable, isMMA=True, keywords=""):
    """
    Analyzes a still frame from a grappling match and generates recommended next moves.
    
    Parameters:
    -----------
    image_path : str
        Path to the image file showing a grappling position
    player_variable : str
        Which player to analyze ('top', 'bottom', or 'both')
    isMMA : bool, optional
        Whether the match is MMA (True) or pure Jiu-jitsu (False)
    keywords : str, optional
        Additional keywords to focus the analysis
        
    Returns:
    --------
    str
        Recommendations for the next immediate steps
    """
    # Get GenAI instance (assuming API key is set via environment variable)
    genai = GenAI(os.environ.get("OPENAI_API_KEY"))
    
    # Create the prompt for image analysis
    match_type = "MMA" if isMMA else "Jiu-jitsu"
    prompt = f"The image is a still frame from a grappling match. The match has {match_type} rules. "
    prompt += f"I want you to analyze: {player_variable}, and provide three options for the next immediate steps "
    prompt += f"towards grappling moves that would work best for them given their current position. "
    prompt += f"I want these steps to be listed in quick bullet format like ex: \"1) <<step>> : towards <<move>>, 2) ...\". "
    prompt += f"Base the recommendations on historical MMA and Jiu-jitsu match performance. "
    
    if keywords:
        prompt += f"I want you to also take special note of the following keywords for your image and recommendation analysis: {keywords}"
    
    # Generate image description with recommendations
    response = genai.generate_image_description(image_path, prompt)
    
    return response


def analyze_grappling_match(video_path, player_variable, isMMA=True, keywords="", start_time=None, end_time=None):
    """
    Analyzes a video of a grappling match and provides feedback and recommendations.
    
    Parameters:
    -----------
    video_path : str
        Path to the video file of the grappling match
    player_variable : str
        Which player to analyze ('top', 'bottom', or 'both')
    isMMA : bool, optional
        Whether the match is MMA (True) or pure Jiu-jitsu (False)
    keywords : str, optional
        Additional keywords to focus the analysis
    start_time : float, optional
        Start time in seconds for video clip extraction
    end_time : float, optional
        End time in seconds for video clip extraction
        
    Returns:
    --------
    str
        Analysis of what went right/wrong and recommendations
    """
    # Get GenAI instance
    genai = GenAI(os.environ.get("OPENAI_API_KEY"))
    
    # Generate a video subset if start_time and end_time are provided
    video_to_analyze = video_path
    if start_time is not None and end_time is not None:
        subset_path = f"{os.path.splitext(video_path)[0]}_subset{os.path.splitext(video_path)[1]}"
        _extract_video_segment(video_path, subset_path, start_time, end_time)
        video_to_analyze = subset_path
    
    # Create the prompt for video analysis
    match_type = "MMA" if isMMA else "Jiu-jitsu"
    prompt = f"These images are frames from a grappling match. The match has {match_type} rules. "
    prompt += f"I want you to analyze: {player_variable}, and provide an analysis of what went right or wrong "
    prompt += f"during the match, along with some recommendations for the {player_variable} in their next match. "
    prompt += f"I want these recommendations to be listed in a quick summary format. "
    prompt += f"Base the recommendations on the athlete's body type, jiu-jitsu guard situation, and historical "
    prompt += f"MMA and Jiu-jitsu match performance. "
    
    if keywords:
        prompt += f"I want you to also take special note of the following keywords for your analysis: {keywords}"
    
    # Generate video description with analysis
    response = genai.generate_video_description(video_to_analyze, prompt)
    
    # Clean up the temporary file if created
    if video_to_analyze != video_path and os.path.exists(video_to_analyze):
        try:
            os.remove(video_to_analyze)
        except:
            pass
    
    return response


def generate_flow_chart(measurables, position_variable="both", isMMA=True, favorite_ideas=""):
    """
    Generates a visual flow chart of jiu-jitsu moves tailored to an athlete's attributes.
    
    Parameters:
    -----------
    measurables : str
        Description of the athlete's physical attributes
    position_variable : str, optional
        Position focus ('top', 'bottom', or 'both')
    isMMA : bool, optional
        Whether to consider MMA (True) or pure Jiu-jitsu (False) ruleset
    favorite_ideas : str, optional
        Athlete's preferred techniques or strategies
        
    Returns:
    --------
    tuple
        (image_url, revised_prompt) - URL to the generated flow chart and the revised prompt
    """
    # Get GenAI instance
    genai = GenAI(os.environ.get("OPENAI_API_KEY"))
    
    # Create the prompt for flow chart generation
    match_type = "MMA" if isMMA else "Jiu-jitsu"
    prompt = f"I want you to generate a visual flow chart of jiu-jitsu moves that will have the greatest likelihood "
    prompt += f"of success for an athlete with the following measurables: {measurables}. "
    prompt += f"I want this chart to focus on {position_variable} position under the {match_type} ruleset"
    
    if favorite_ideas:
        prompt += f", and take into account that the athlete has the following ideas: {favorite_ideas}"
    
    # Generate the flow chart image
    image_url, revised_prompt = genai.generate_image(prompt)
    
    return image_url, revised_prompt


def gracie_talk(gracie_name, chat_history, user_message):
    """
    Simulates a conversation with a specified Gracie family member about grappling and self-defense.
    
    Parameters:
    -----------
    gracie_name : str
        Name of the Gracie family member to simulate
    chat_history : list
        List of previous messages, each as a dict with "role" and "content"
    user_message : str
        The latest message from the user
        
    Returns:
    --------
    str
        Response from the simulated Gracie family member
    """
    # Get GenAI instance
    genai = GenAI(os.environ.get("OPENAI_API_KEY"))
    
    # Create the instructions for the chat
    instructions = f"You are the famous martial arts practitioner {gracie_name}. "
    instructions += f"I want you to have a conversation with the user based on that information, "
    instructions += f"and have the conversation focused around improving the user's grappling and self-defense. "
    instructions += f"I want the conversation to always have an upbeat and motivational conversational style."
    
    # Generate chat response
    response = genai.generate_chat_response(chat_history, user_message, instructions)
    
    return response


def estimate_athlete_measurements(image_path, position_descriptor=""):
    """
    Estimates the height and weight of an athlete from an image.
    
    Parameters:
    -----------
    image_path : str
        Path to the image file showing the athlete
    position_descriptor : str, optional
        Description of which athlete to analyze in case of multiple people 
        (e.g., "in blue gi", "on the left", "the top position fighter")
        
    Returns:
    --------
    str
        Estimated height, weight, and physical attributes of the athlete
    """
    # Get GenAI instance
    genai = GenAI(os.environ.get("OPENAI_API_KEY"))
    
    # Create the prompt for athlete measurement estimation
    prompt = "Please analyze this image and provide an estimate of the "
    
    if position_descriptor:
        prompt += f"athlete {position_descriptor}'s "
    else:
        prompt += "athlete's "
    
    prompt += "height, weight, and build. Include details about their body type "
    prompt += "(such as endomorph, mesomorph, ectomorph), muscle mass distribution, limb length proportions, "
    prompt += "and any notable physical characteristics that might affect their performance in grappling. "
    prompt += "Present your analysis in a clear, concise format with estimates for height in feet/inches and cm, "
    prompt += "weight in pounds and kg, and body type classification."
    
    # Generate image description with physical measurements
    response = genai.generate_image_description(image_path, prompt)
    
    return response


def _extract_video_segment(input_path, output_path, start_time, end_time):
    """
    Helper function to extract a segment from a video between specified start and end times.
    
    Parameters:
    -----------
    input_path : str
        Path to the input video file
    output_path : str
        Path where the output video segment will be saved
    start_time : float
        Start time in seconds
    end_time : float
        End time in seconds
        
    Returns:
    --------
    bool
        True if extraction was successful, False otherwise
    """
    try:
        # Open the video file
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            return False
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID' for AVI
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Calculate frame numbers for start and end time
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        
        # Set frame position to start_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        current_frame = start_frame
        while current_frame <= end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            
            out.write(frame)
            current_frame += 1
            
        # Release everything
        cap.release()
        out.release()
        
        return True
    
    except Exception as e:
        print(f"Error extracting video segment: {e}")
        return False