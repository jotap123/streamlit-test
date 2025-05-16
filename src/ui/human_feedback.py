import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="LLM Legal Analysis Feedback System",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state variables
if 'current_evaluation_index' not in st.session_state:
    st.session_state.current_evaluation_index = 0
if 'evaluations' not in st.session_state:
    # This would typically be loaded from a database or file
    st.session_state.evaluations = []
if 'feedback_history' not in st.session_state:
    st.session_state.feedback_history = []
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

# Functions for file management
def save_feedback(feedback_data):
    """Save feedback to a JSON file"""
    feedback_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create directory if it doesn't exist
    if not os.path.exists('feedback_data'):
        os.makedirs('feedback_data')
    
    # Generate filename with timestamp
    filename = f"feedback_data/feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(feedback_data, f, indent=4)
    
    # Also append to feedback history
    st.session_state.feedback_history.append(feedback_data)
    
    return filename

def load_evaluations(uploaded_file):
    """Load evaluations from uploaded file"""
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.json'):
                data = json.load(uploaded_file)
                if isinstance(data, list):
                    st.session_state.evaluations = data
                    st.session_state.current_evaluation_index = 0
                    return True
                else:
                    st.error("The JSON file must contain a list of evaluations")
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                required_columns = ['user_message', 'ai_response', 'agent_evaluation']
                if all(col in df.columns for col in required_columns):
                    st.session_state.evaluations = df.to_dict('records')
                    st.session_state.current_evaluation_index = 0
                    return True
                else:
                    st.error(f"CSV must have these columns: {', '.join(required_columns)}")
            else:
                st.error("Please upload a JSON or CSV file")
        except Exception as e:
            st.error(f"Error loading file: {e}")
    return False

# Main app header
st.title("🤖 LLM Agent Evaluation Feedback System")
st.write("Review how the LLM Agent evaluates human-AI interactions and provide expert feedback to improve the evaluation process")

# Sidebar for navigation and controls
with st.sidebar:
    st.header("Controls")
    
    # File upload for evaluations
    st.subheader("Load Evaluations")
    uploaded_file = st.file_uploader("Upload evaluations (JSON or CSV)", type=['json', 'csv'])
    if uploaded_file:
        if load_evaluations(uploaded_file):
            st.success(f"Loaded {len(st.session_state.evaluations)} evaluations")
    
    # Add sample data button for demo purposes
    if st.button("Load Sample Data"):
        st.session_state.evaluations = [
            {
                "evaluation_id": "eval001",
                "user_message": "Can you explain the concept of machine learning in simple terms?",
                "ai_response": "Machine learning is like teaching a computer to learn from examples rather than programming explicit instructions. Imagine instead of telling a computer step-by-step how to recognize a cat, you show it thousands of cat pictures and it learns the patterns itself.",
                "agent_evaluation": "The AI provided a clear and accessible explanation of machine learning using an appropriate analogy. The response is concise and addresses the user's question directly without unnecessary technical jargon. However, the explanation could have been improved by briefly mentioning different types of machine learning approaches or including a simple practical example of machine learning application.",
                "topic": "Educational query",
                "subtopic": "Machine Learning"
            },
            {
                "evaluation_id": "eval002",
                "user_message": "I'm feeling really depressed today and don't know what to do.",
                "ai_response": "I'm sorry to hear you're feeling depressed. While I can suggest some self-care activities like taking a walk or connecting with friends, depression is serious and often requires professional help. Have you considered speaking with a mental health professional? They can provide personalized support and strategies.",
                "agent_evaluation": "The AI response appropriately acknowledges the user's emotional state and shows empathy. It correctly emphasizes the importance of professional help for depression rather than positioning itself as a mental health advisor. The response provides brief self-care suggestions while prioritizing professional support. This approach is well-balanced and responsible for a sensitive mental health query.",
                "topic": "Mental health query",
                "subtopic": "Depression"
            },
            {
                "evaluation_id": "eval003",
                "user_message": "What are some good investment strategies for beginners?",
                "ai_response": "For beginners, consider: 1) Start with low-cost index funds that track the broader market, 2) Set up automatic contributions to take advantage of dollar-cost averaging, 3) Diversify across different asset types, 4) Only invest money you won't need in the near future, and 5) Consider speaking with a financial advisor for personalized advice.",
                "agent_evaluation": "The AI provides generic investment advice commonly found in beginner financial education materials. While the recommendations follow generally accepted principles, the response lacks disclaimers about financial risk and could be more explicit about the AI not providing personalized financial advice. The inclusion of consulting a financial advisor is appropriate, but should be more prominently featured. The numbered format makes the response easy to follow.",
                "topic": "Financial advice query",
                "subtopic": "Investing"
            }
        ]
        st.session_state.current_evaluation_index = 0
        st.success("Loaded sample evaluations")

    # Navigation controls (only shown if evaluations are loaded)
    if st.session_state.evaluations:
        st.subheader("Navigation")
        total_evaluations = len(st.session_state.evaluations)
        
        st.write(f"Viewing evaluation {st.session_state.current_evaluation_index + 1} of {total_evaluations}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous", disabled=st.session_state.current_evaluation_index <= 0):
                st.session_state.current_evaluation_index -= 1
        with col2:
            if st.button("Next", disabled=st.session_state.current_evaluation_index >= total_evaluations - 1):
                st.session_state.current_evaluation_index += 1
        
        # Jump to specific evaluation
        selected_index = st.number_input("Go to evaluation", 
                                        min_value=1, 
                                        max_value=total_evaluations,
                                        value=st.session_state.current_evaluation_index + 1) - 1
        if selected_index != st.session_state.current_evaluation_index:
            st.session_state.current_evaluation_index = selected_index
    
    # Toggle feedback history view
    if st.button("View Feedback History" if not st.session_state.show_history else "Hide Feedback History"):
        st.session_state.show_history = not st.session_state.show_history

# Main content area - show if evaluations are loaded
if st.session_state.evaluations:
    # Get current evaluation
    current_idx = st.session_state.current_evaluation_index
    current_evaluation = st.session_state.evaluations[current_idx]
    
    # Display the three-layer structure
    st.header("Original Human-AI Interaction")
    
    # Show evaluation ID if available
    if "evaluation_id" in current_evaluation:
        st.info(f"Evaluation ID: {current_evaluation['evaluation_id']}")
    
    # Show topic if available
    if "topic" in current_evaluation:
        st.subheader("Topic")
        st.write(current_evaluation["topic"])
    
    # Show subtopic if available
    if "subtopic" in current_evaluation:
        st.subheader("Subtopic")
        st.write(current_evaluation["subtopic"])
    
    # Original interaction
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("User Message")
        st.write(current_evaluation["user_message"])
    
    with col2:
        st.subheader("AI Response")
        st.write(current_evaluation["ai_response"])
    
    # LLM Agent's evaluation
    st.header("LLM Agent's Evaluation")
    with st.expander("View Agent Evaluation", expanded=True):
        st.write(current_evaluation["agent_evaluation"])
    
    # Human expert feedback form
    st.header("Your Expert Feedback on Agent's Evaluation")
    
    with st.form("feedback_form"):
        # Overall assessment of agent's evaluation
        evaluation_quality = st.slider(
            "Overall Quality of Agent's Evaluation", 
            1, 3, 2, 
            help="1= Poor, 2= Fair, 3= Good",
        )
        
        # Multi-select for strengths and weaknesses of the evaluation
        evaluation_strengths = st.multiselect(
            "Strengths of the Agent's Evaluation",
            options=[
                "Comprehensive assessment", 
                "Complete", 
                "Well-reasoned critique",
                "Balanced feedback", 
                "Good technical analysis",
            ]
        )
        
        evaluation_weaknesses = st.multiselect(
            "Weaknesses of the Agent's Evaluation",
            options=[
                "Didn't address the IRAC framework", 
                "Very extensive explanation", 
                "Too lenient/uncritical",
                "Overlooked context", 
                "Safety concerns not addressed",
                "Ethical dimensions ignored",
                "Too vague/general",
                "Inconsistent assessment criteria",
                "Focus on wrong aspects"
            ]
        )
        
        # Detailed feedback sections
        col1, col2 = st.columns(2)
        
        with col1:
            issue_assessment = st.radio(
                "The Agent's issue assessment was:",
                ["Accurate", "Partially accurate", "Inaccurate", "Missing"],
                index=0
            )
            
            rationale_assessment = st.radio(
                "The Agent's rationale assessment was:",
                ["Thorough", "Adequate", "Insufficient", "Missing", "Not applicable"],
                index=1
            )
        
        with col2:
            application_assessment = st.radio(
                "The Agent's application assessment was:",
                ["Thorough", "Adequate", "Insufficient", "Missing", "Not applicable"],
                index=0
            )
            
            conclusion = st.radio(
                "The Agent's conclusion was:",
                ["Spot-on", "Decent", "Lacking", "Inconsistent", "Missing"],
                index=0
            )
        
        # General feedback
        feedback_notes = st.text_area(
            "Feedback for the LLM Agent",
            help="Provide any additional feedback or training guidance to improve the LLM Agent's future evaluations",
            height=150
        )
        
        # Submit button
        submitted = st.form_submit_button("Submit Expert Feedback")
        
        if submitted:
            # Gather feedback into a structured format
            feedback_data = {
                "evaluation_id": current_evaluation.get("evaluation_id", f"evaluation_{current_idx}"),
                "original_interaction": {
                    "user_message": current_evaluation["user_message"],
                    "ai_response": current_evaluation["ai_response"],
                    "topic": current_evaluation.get("topic", ""),
                    "subtopic": current_evaluation.get("subtopic", "")
                },
                "agent_evaluation": current_evaluation["agent_evaluation"],
                "expert_feedback": {
                    "overall_quality": evaluation_quality,
                    "strengths": evaluation_strengths,
                    "weaknesses": evaluation_weaknesses,
                    "issue_assessment": issue_assessment,
                    "rationale_assessment": rationale_assessment,
                    "application_assessment": application_assessment,
                    "conclusion": conclusion,
                    "feedback": feedback_notes
                }
            }
            
            # Save feedback
            saved_file = save_feedback(feedback_data)
            st.success(f"Feedback submitted and saved to {saved_file}")
            
            # Auto-advance to next evaluation if available
            if current_idx < len(st.session_state.evaluations) - 1:
                st.session_state.current_evaluation_index += 1
                st.experimental_rerun()

# Display feedback history if toggled
if st.session_state.show_history and st.session_state.feedback_history:
    st.header("Feedback History")
    
    for i, feedback in enumerate(st.session_state.feedback_history):
        with st.expander(f"Feedback #{i+1} - {feedback.get('evaluation_id', 'Unknown')}"):
            # Show compact version of the original interaction
            st.subheader("Original Interaction Summary")
            st.write(f"**User Query:** {feedback['original_interaction']['user_message'][:100]}...")
            
            # Show compact version of agent evaluation
            st.subheader("Agent Evaluation")
            st.write(f"{feedback['agent_evaluation'][:150]}...")
            
            # Expert feedback summary
            st.subheader("Your Expert Feedback")
            st.write(f"**Overall Quality Rating:** {feedback['expert_feedback']['overall_quality']}/10")
            
            # Strengths and weaknesses
            if feedback['expert_feedback']['strengths']:
                st.write("**Evaluation Strengths:** " + ", ".join(feedback['expert_feedback']['strengths']))
            
            if feedback['expert_feedback']['weaknesses']:
                st.write("**Evaluation Weaknesses:** " + ", ".join(feedback['expert_feedback']['weaknesses']))
            
            # Assessment details in columns
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Accuracy Assessment:** {feedback['expert_feedback']['accuracy_assessment']}")
                st.write(f"**Safety Assessment:** {feedback['expert_feedback']['safety_assessment']}")
            
            with col2:
                st.write(f"**Helpfulness Assessment:** {feedback['expert_feedback']['helpfulness_assessment']}")
                st.write(f"**Critique Balance:** {feedback['expert_feedback']['critique_balance']}")
            
            # Show improved evaluation if provided
            if feedback['expert_feedback']['improved_evaluation']:
                with st.expander("View Improved Evaluation"):
                    st.write(feedback['expert_feedback']['improved_evaluation'])
            
            # Show additional guidance if provided
            if feedback['expert_feedback']['additional_guidance']:
                with st.expander("View Additional Guidance"):
                    st.write(feedback['expert_feedback']['additional_guidance'])
            
            st.write(f"_Submitted on: {feedback.get('timestamp', 'Unknown time')}_")

# Show instructions if no evaluations are loaded
else:
    st.info("Please load evaluation data using the sidebar controls.")
    
    st.markdown("""
    ## Instructions
    
    This application helps human experts provide feedback on how an LLM Agent evaluates human-AI interactions.
    
    ### What's being evaluated:
    1. **First layer:** Original interaction between a human user and an AI system
    2. **Second layer:** LLM Agent's evaluation of that interaction
    3. **Third layer:** YOUR expert feedback on the LLM Agent's evaluation
    
    ### To get started:
    1. Upload a JSON or CSV file containing the evaluations data
    2. Or click "Load Sample Data" to see example evaluations
    3. Review each interaction, the LLM Agent's evaluation, and provide your expert feedback
    4. Navigate between evaluations using the sidebar controls
    
    ### Expected data format:
    - **JSON**: A list of objects with at least `user_message`, `ai_response`, and `agent_evaluation` fields
    - **CSV**: A table with at least `user_message`, `ai_response`, and `agent_evaluation` columns
    
    ### Optional fields:
    - `evaluation_id`: A unique identifier for the evaluation
    - `context`: Additional context about the interaction
    
    Your feedback will be saved in JSON format in a `feedback_data` folder.
    """)