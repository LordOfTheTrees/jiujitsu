import os
from genai import GenAI

def generate_grappling_plan(image, player_variable, isMMA=True, keywords=""):
    """
    Analyzes a still frame from a grappling match and generates recommended next moves.
    
    Parameters:
    -----------
    image : str
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
    prompt = f"the image is a still frame from a grappling match. The match has {match_type} rules. "
    prompt += f"I want you to analyze: {player_variable}, and provide three options for the next immediate steps "
    prompt += f"towards grappling moves that would work best for them given their current position. "
    prompt += f"I want these steps to be listed in quick bullet format like ex: \"1) <<step>> : towards <<move>>, 2) ...\". "
    prompt += f"Base the recommendations on historical MMA and Jiu-jitsu match performance. "
    
    if keywords:
        prompt += f"I want you to also take special note of the following keywords for your image and recommendation analysis: {keywords}"
    
    # Generate image description with recommendations
    response = genai.generate_image_description(image, prompt)
    
    return response


def analyse_grappling_match(video, player_variable, isMMA=True, keywords="", start_time=None, end_time=None):
    """
    Analyzes a video of a grappling match and provides feedback and recommendations.
    
    Parameters:
    -----------
    video : str
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
    video_to_analyze = video
    if start_time is not None and end_time is not None:
        # Extract frames for the specified time range
        # This is a simplification as we can't directly create a subset video without FFmpeg
        pass
    
    # Create the prompt for video analysis
    match_type = "MMA" if isMMA else "Jiu-jitsu"
    prompt = f"these images are frames from a grappling match. The match has {match_type} rules. "
    prompt += f"I want you to analyze: {player_variable}, and provide an analysis of what went right or wrong "
    prompt += f"during the match, along with some recommendations for the {player_variable} in their next match. "
    prompt += f"I want these recommendations to be listed in a quick summary format. "
    prompt += f"Base the recommendations on the athlete's body type, jiu-jitsu guard situation, and historical "
    prompt += f"MMA and Jiu-jitsu match performance. "
    
    if keywords:
        prompt += f"I want you to also take special note of the following keywords for your analysis: {keywords}"
    
    # Generate video description with analysis
    response = genai.generate_video_description(video_to_analyze, prompt)
    
    return response


def generate_flow_chart(measurables, position_variable="both", isMMA=True, favorite_ideas=""):
    """
    Generates a Mermaid-based radial flow chart of jiu-jitsu moves tailored to an athlete's attributes.
    
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
    str
        Mermaid object code for the flow chart
    """
    # Get GenAI instance
    genai = GenAI(os.environ.get("OPENAI_API_KEY"))
    
    # Create the prompt for flow chart generation
    match_type = "MMA" if isMMA else "Jiu-jitsu"
    prompt = f"I want you to generate a Mermaid based radial visual flow chart of jiu-jitsu moves that will have the greatest likelihood "
    prompt += f"of success for an athlete with the following measurables: {measurables}. "
    prompt += f"I want this chart to focus on {position_variable} under the {match_type} ruleset"
    
    if favorite_ideas:
        prompt += f", and take into account that the athlete has the following ideas: {favorite_ideas}"
    
    # Add specific instructions for the output format
    prompt += " of the athlete. Could you label the flow arrows in the diagram using a description of the primary movement required to get to that bubble. Only return the mermaid object, and not any shoulder text whatsoever"
    
    # Generate the mermaid object
    mermaid_object = genai.generate_text(prompt)
    
    return mermaid_object


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
    prompt = f"you are the famous martial arts practitioner {gracie_name}. "
    prompt += f"I want you to have a conversation with the user based on that information, "
    prompt += f"and have the conversation focused around improving the user's grappling and self-defense. "
    prompt += f"I want the conversation to always have an upbeat and motivational conversational style."
    
    # Generate chat response
    response = genai.generate_chat_response(chat_history, user_message, prompt)
    
    return response


def generate_mermaid(mermaid_object):
    """
    Converts a Mermaid object string into a displayable JavaScript-based Mermaid object.
    
    Parameters:
    -----------
    mermaid_object : str
        String containing the Mermaid diagram code
        
    Returns:
    --------
    object
        JavaScript-based Mermaid object ready for display
    """
    # This is a placeholder for the actual implementation
    # In a real application, this would convert the Mermaid string into a renderable object
    # For example, using JavaScript libraries or a backend service
    
    # Clean up the mermaid object (remove markdown backticks if present)
    if "```mermaid" in mermaid_object:
        mermaid_object = mermaid_object.replace("```mermaid", "").replace("```", "").strip()
    
    # Here you would integrate with a Mermaid rendering library
    # For now, we'll return the cleaned mermaid string
    return mermaid_object


def display_graph(flow_chart):
    """
    Displays a Mermaid flow chart as an HTML object.
    
    Parameters:
    -----------
    flow_chart : object
        Mermaid object to be displayed
        
    Returns:
    --------
    str
        HTML string that can be used to display the chart
    """
    # Create HTML representation of the Mermaid chart
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jiu-Jitsu Flow Chart</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose',
            }});
        </script>
        <style>
            .mermaid {{
                width: 100%;
                height: auto;
                overflow: auto;
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
        {flow_chart}
        </div>
    </body>
    </html>
    """
    
    return html


def next_move(flow_chart, move_text, measurables, isMMA=True, favorite_ideas=""):
    """
    Generates a new flow chart based on the selected move from an existing chart.
    
    Parameters:
    -----------
    flow_chart : str
        Mermaid object representing the current flow chart
    move_text : str
        Text of the selected move
    measurables : str
        Description of the athlete's physical attributes
    isMMA : bool, optional
        Whether to consider MMA (True) or pure Jiu-jitsu (False) ruleset
    favorite_ideas : str, optional
        Athlete's preferred techniques or strategies
        
    Returns:
    --------
    str
        Updated Mermaid object for the new flow chart
    """
    # Parse the flow chart to find the next node
    # This is a simplified implementation and would need more robust parsing in a real application
    
    # For demonstration, extract the target node
    lines = flow_chart.strip().split('\n')
    new_position = None
    
    for line in lines:
        if move_text in line and "-->" in line:
            parts = line.split("-->")
            if len(parts) >= 2:
                # Extract the target node (removing any labels)
                target = parts[1].strip()
                if "[" in target:
                    new_position = target.split("[")[0].strip()
                else:
                    new_position = target
                break
    
    # If no next node found, return the original chart
    if not new_position:
        return flow_chart
    
    # Generate a new flow chart with the found position as the center
    return generate_flow_chart(measurables, new_position, isMMA, favorite_ideas)


def get_attributes(image, player_variable):
    """
    Analyzes an image to estimate the physical attributes of an athlete.
    
    Parameters:
    -----------
    image : str
        Path to the image file showing a grappling match
    player_variable : str
        Which player to analyze ('top', 'bottom', or 'both')
        
    Returns:
    --------
    str
        Estimated height, weight, and physical attributes of the athlete
    """
    # Get GenAI instance
    genai = GenAI(os.environ.get("OPENAI_API_KEY"))
    
    # Create the prompt for athlete measurement estimation
    prompt = f"Please analyze this grappling match image and provide an estimate of the {player_variable} athlete's "
    prompt += "height, weight, and build. Include details about their body type "
    prompt += "(such as endomorph, mesomorph, ectomorph), muscle mass distribution, limb length proportions, "
    prompt += "and any notable physical characteristics that might affect their performance in grappling. "
    prompt += "Present your analysis in a clear, concise format with estimates for height in feet/inches and cm, "
    prompt += "weight in pounds and kg, and body type classification."
    
    # Generate image description with physical measurements
    response = genai.generate_image_description(image, prompt)
    
    return response