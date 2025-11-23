# app.py
"""
Account Plan Generator with Chat Interface
Requires: streamlit, agent module with process_user_message function
"""

import streamlit as st
from agent import process_user_message

st.set_page_config(
    page_title="Account Plan Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# DARK MODE CSS (ENHANCED)
# -------------------------------
st.markdown(
    """
    <style>

    /* Full Background Dark */
    body, .stApp {
        background-color: #0d0d0d !important;
        color: #ffffff !important;
    }

    /* Sidebar + main container */
    .main, .block-container {
        background-color: #0d0d0d !important;
        padding-top: 2rem !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Chat bubbles */
    .user-msg {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin-bottom: 10px;
        margin-left: auto;
        width: fit-content;
        max-width: 80%;
        box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3);
        animation: slideInRight 0.3s ease-out;
    }

    .bot-msg {
        background: #2c2c2c;
        color: #e0e0e0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin-bottom: 10px;
        margin-right: auto;
        width: fit-content;
        max-width: 80%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        animation: slideInLeft 0.3s ease-out;
    }

    /* Message animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Chat container */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 20px;
        max-height: 70vh;
        overflow-y: auto;
        padding: 10px;
    }

    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }

    .chat-container::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 10px;
    }

    .chat-container::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 10px;
    }

    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    /* Chat header title */
    .chat-title {
        font-size: 28px;
        font-weight: 700;
        padding-bottom: 20px;
        color: #f5f5f5;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* Account plan formatting */
    .account-plan-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 20px;
        color: #f5f5f5;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 8px;
        color: #64b5f6;
    }

    /* Account plan container */
    .plan-container {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 20px;
        max-height: 75vh;
        overflow-y: auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    .plan-container::-webkit-scrollbar {
        width: 8px;
    }

    .plan-container::-webkit-scrollbar-track {
        background: #0d0d0d;
        border-radius: 10px;
    }

    .plan-container::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 10px;
    }

    /* Empty state */
    .empty-state {
        opacity: 0.5;
        text-align: center;
        padding: 40px 20px;
        font-style: italic;
    }

    /* Input field styling */
    .stChatInputContainer {
        border-top: 1px solid #2c2c2c;
        padding-top: 10px;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%) !important;
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4) !important;
    }

    /* Download button specific styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%) !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4) !important;
    }

    /* Fix for button text color */
    .stButton button p,
    .stDownloadButton button p,
    .stButton button span,
    .stDownloadButton button span {
        color: white !important;
    }

    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        padding: 12px 18px;
        background: #2c2c2c;
        border-radius: 18px;
        margin-bottom: 10px;
    }

    .typing-indicator span {
        height: 8px;
        width: 8px;
        background-color: #64b5f6;
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: typing 1.4s infinite;
    }

    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "account_plan" not in st.session_state:
    st.session_state.account_plan = ""

if "processing" not in st.session_state:
    st.session_state.processing = False

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def render_chat_messages():
    """Render all chat messages with proper styling"""
    chat_html = "<div class='chat-container'>"
    
    for role, msg in st.session_state.messages:
        msg_escaped = msg.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        
        if role == "user":
            chat_html += f"<div class='user-msg'>🧑 <strong>You:</strong><br>{msg_escaped}</div>"
        else:
            chat_html += f"<div class='bot-msg'>🤖 <strong>Assistant:</strong><br>{msg_escaped}</div>"
    
    # Add typing indicator if processing
    if st.session_state.processing:
        chat_html += """
        <div class='typing-indicator'>
            <span></span>
            <span></span>
            <span></span>
        </div>
        """
    
    chat_html += "</div>"
    return chat_html

def clear_chat():
    """Clear chat history and account plan"""
    st.session_state.messages = []
    st.session_state.account_plan = ""
    st.rerun()

def download_plan():
    """Generate downloadable PDF content for the account plan"""
    if st.session_state.account_plan:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor
        import io
        import re
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1e88e5'),
            spaceAfter=30,
            alignment=1,  # Center alignment
            fontName='Helvetica-Bold'
        )
        
        # Custom heading style
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#2c2c2c'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        # Custom body style
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=HexColor('#333333'),
            spaceAfter=12,
            leading=14
        )
        
        # Parse HTML content
        content = st.session_state.account_plan
        
        # Add title
        story.append(Paragraph("Account Plan", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Simple HTML to PDF conversion
        # Split by common HTML tags and format accordingly
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Remove HTML tags but detect their type
            clean_line = re.sub('<[^<]+?>', '', line)
            clean_line = clean_line.replace('&nbsp;', ' ').strip()
            
            if not clean_line:
                continue
            
            # Detect if it's a heading (contains bold or section markers)
            if any(tag in line.lower() for tag in ['<h1', '<h2', '<h3', '<strong>', '<b>']):
                story.append(Paragraph(clean_line, heading_style))
            else:
                story.append(Paragraph(clean_line, body_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    return None

# -------------------------------
# LAYOUT: LEFT CHAT — RIGHT PLAN
# -------------------------------
left, right = st.columns([0.55, 0.45], gap="large")

with left:
    # Header with clear button
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown("<div class='chat-title'> CorpResearch AI — Company Research Chatbot</div>", unsafe_allow_html=True)
    with col2:
        if st.button(" Clear", help="Clear chat history"):
            clear_chat()
    
    # Display chat history
    st.markdown(render_chat_messages(), unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Type your message…", disabled=st.session_state.processing)

    if user_input and not st.session_state.processing:
        # Set processing flag
        st.session_state.processing = True
        
        # Save user message
        st.session_state.messages.append(("user", user_input))
        st.rerun()

    # Process message if in processing state
    if st.session_state.processing and st.session_state.messages:
        last_role, last_msg = st.session_state.messages[-1]
        
        if last_role == "user":
            try:
                # Process using agent
                bot_reply, updated_plan = process_user_message(
                    last_msg,
                    current_plan=st.session_state.account_plan
                )
                
                # Save bot reply
                st.session_state.messages.append(("assistant", bot_reply))
                
                # Update account plan if provided
                if updated_plan:
                    st.session_state.account_plan = updated_plan
                
            except Exception as e:
                error_msg = f"⚠️ An error occurred: {str(e)}"
                st.session_state.messages.append(("assistant", error_msg))
            
            finally:
                # Reset processing flag
                st.session_state.processing = False
                st.rerun()

with right:
    # Header with download button
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown("<div class='account-plan-title'> Generated Account Plan</div>", unsafe_allow_html=True)
    with col2:
        if st.session_state.account_plan:
            plan_pdf = download_plan()
            if plan_pdf:
                st.download_button(
                    label=" Download",
                    data=plan_pdf,
                    file_name="account_plan.pdf",
                    mime="application/pdf",
                    help="Download account plan as PDF file"
                )
    
    # Display account plan
    if st.session_state.account_plan:
        st.markdown(
            f"<div class='plan-container'>{st.session_state.account_plan}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='plan-container'><div class='empty-state'>💡 Your account plan will appear here after you request one from the assistant...</div></div>",
            unsafe_allow_html=True
        )