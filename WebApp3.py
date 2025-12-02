import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os
import base64
import altair as alt # <-- Added import for charts
import sys

# -------------------------------
# 1. FILE PATHS AND INITIALIZATION
# -------------------------------
MODEL_PATH = "C:/Users/Sherylle Rose/Desktop/rfmodeloct26/rf_model.pkl"
VECTORIZER_PATH = "C:/Users/Sherylle Rose/Desktop/rfmodeloct26/vectorizer.pkl"
# --- Logo Paths ---
HOME_LOGO_PATH = "C:/Users/Sherylle Rose/homeplogo.png"
SIDEBAR_LOGO_PATH = "C:\\Users\\Sherylle Rose\\ccitlogo.png"
# --- Background Image Path (Set your path here) ---
BACKGROUND_IMAGE_PATH = "C:\\Users\\Sherylle Rose\\bg_final.png"
# ---------------------------------------------------

# Define Original/Standard Colors
LIGHT_BG = "#e8f3f8"
DARK_PRIMARY = "#1f3a52" # <-- This is the color used for the dark blue elements
ACCENT_BLUE = "#1f7fc1" # <-- This color will be used for the graph bars and table header

# Function to convert local file to Base64 string
def get_base64_of_file(path):
    """Encodes a local file to a Base64 string for CSS embedding."""
    try:
        if not os.path.exists(path):
            st.error(f"Error: Background file not found at: {path}. Please check the path and run the script again.")
            return None
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error encoding background file: {e}")
        return None

# Load model and vectorizer only once
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except FileNotFoundError:
    st.error("Error: Model or vectorizer file not found. Please check paths.")
    model = None
    vectorizer = None

# Get Base64 string for the background image
bg_base64 = get_base64_of_file(BACKGROUND_IMAGE_PATH)


# -------------------------------
# 2. HISTORY FILE INITIALIZATION
# -------------------------------
HISTORY_FILE = "sentiment_history.csv"
if not os.path.exists(HISTORY_FILE):
    try:
        pd.DataFrame(columns=["Date", "Time", "Response", "Classification"]).to_csv(HISTORY_FILE, index=False)
    except Exception as e:
        st.error(f"Critical initialization error: Could not create empty history file. Error: {e}")


# -------------------------------
# 3. STREAMLIT PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Competence Sentiment Analyzer", layout="wide")


# -------------------------------
# 4. UI STYLE – GLOBAL (Non-Conditional CSS)
# -------------------------------

# Apply light background color globally to the overall app view container
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: {LIGHT_BG} !important;
}}
.stApp {{
    background-color: transparent !important;
}}

/* -------- GLOBAL (Main CSS block) -------- */
body, [data-testid="stAppViewContainer"] {{
    font-family: 'Arial', sans-serif; /* ⭐ FONT CHANGED TO ARIA HERE ⭐ */
    color: {DARK_PRIMARY} !important;
}}

/* 1. AGGRESSIVE REMOVAL OF TOP PADDING (Targeting main block containers) */
.css-18e3th9, .css-1d391kg, .block-container, 
[data-testid="stVerticalBlock"] > div:first-child > div:first-child {{
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}}

/* -------- NEW CSS FOR HOME PAGE LOGO SPACING -------- */
.home-logo-container img {{
    margin-top: 0px !important;
    margin-bottom:-50px !important; /* This helps pull content below the image up */
    padding: 0px !important;
}}

/* ⬇️ ADJUSTMENT APPLIED HERE: Thinner Sidebar ⬇️ */
[data-testid="stSidebar"] {{
    background: {DARK_PRIMARY} !important;
    width: 20px !important; /* Made even thinner: 20px */
    padding: 5px 5px 50px 5px !important; /* Adjusted padding */
    display: flex;
    flex-direction: column;
    align-items: center; 
}}

/* ---------------------------------------------------- */
/* NEW/ADJUSTED CSS FOR LOGO POSITIONING (SIDEBAR) */
/* ---------------------------------------------------- */
[data-testid="stSidebar"] img {{
    display: block; 
    margin-left: auto;
    margin-right: auto;
    width: 55% !important; 
    max-width: 50px; 
    padding-top: 10px; 
    padding-bottom: 40px; 
}}


/* 3. Cleanup spacing around buttons in the sidebar */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    gap: 0px; 
}}

/* ⭐ CRITICAL FIX: Ensure the navigation container is centered/aligned ⭐ */
[data-testid="stSidebarNavItems"] {{
    /* ALIGNMENT CHANGES HERE TO CENTER THE BUTTONS */
    width: 100%; /* Ensure it takes full width for centering */
    align-items: center !important; /* Center the buttons block */
    padding-left: 0px !important;
}}

/* Sidebar buttons - Base Style */
[data-testid="stSidebar"] div.stButton > button {{
    background: transparent !important;
    border: none !important;
    font-size: 30px !important;
    color: #e7f3fa !important;
    width: 100%;
    
    /* ⭐ CENTER BUTTON STYLES ⭐ */
    max-width: 150px; /* Define maximum width for the button */
    margin-right: auto; /* Auto margin for centering */
    margin-left: auto !important; /* Auto margin for centering (overrides existing) */
    
    /* ⭐ KEEP TEXT/ICON LEFT ALIGNED INSIDE BUTTON ⭐ */
    text-align: left !important; 
    padding: 10px 0px 10px 0px !important; 
    line-height: 1.0; 
    display: flex !important;
    justify-content: flex-start !important;
    /* margin-left: -10px !important; REMOVED/OVERRIDDEN */
}}

/* Sidebar buttons - Hover State */
[data-testid="stSidebar"] div.stButton > button:hover {{
    background: rgba(255,255,255,0.15) !important;
    border-radius: 0px !important;
}}

/* ⭐ NEW: Active/Selected State CSS ⭐ */
.active-sidebar-button > button {{
    background: rgba(255,255,255,0.15) !important;
    border-radius: 0px !important;
}}

/* -------- HEADINGS (Aggressive negative margin for H1 to pull it closer to the logo) -------- */
h1 {{ 
    font-size: 55px !important; 
    color: {DARK_PRIMARY} !important; 
    font-weight: 700; 
    margin-top: -50px !important; 
    margin-bottom: 5px;
    text-align: center; 
}}
h2 {{ font-size: 32px !important; color: {DARK_PRIMARY} !important; }}
h3 {{ font-size: 28px !important; color: {DARK_PRIMARY} !important; }}

/* Input Area (Default Style) */
textarea, .stTextInput input {{
    background: white !important;
    border: 3px solid #c7d9e2 !important;
    border-radius: 12px !important;
    color: {DARK_PRIMARY} !important;
    font-size: 18px !important;
    padding: 14px !important;
}}

/* ⭐ BORDER AND TEXT COLOR FIX: Dark blue border/text when active/hover ⭐ */
textarea:focus, textarea:hover, 
.stTextInput input:focus, .stTextInput input:hover {{
    border: 3px solid {DARK_PRIMARY} !important; /* Border color set to dark blue */
    color: {DARK_PRIMARY} !important; /* Text color set to dark blue */
    outline: none !important; /* Remove default focus outline */
}}

/* ⭐ FIX: Target the Streamlit internal container for text area to remove red/change border color on focus/hover ⭐ */
[data-testid="stTextarea"] > div > div:focus, 
[data-testid="stTextarea"] > div > div:focus-within,
[data-testid="stTextarea"] > div > div:hover {{
    border-color: {DARK_PRIMARY} !important; 
    box-shadow: none !important; 
}}
textarea:focus {{
    border: 3px solid {DARK_PRIMARY} !important;
}}


/* BIG LABEL FOR TEXT AREA */
.big-label label {{
    font-size: 40px !important; 
    font-weight: 700 !important;
    color: {DARK_PRIMARY} !important;
    margin-bottom: 10px;
}}

/* Tables - GLOBAL */
table, th, td {{ color: {DARK_PRIMARY} !important; }}
th {{ background: {ACCENT_BLUE} !important; color: white !important; }}
</style>

<style>
/* -------- FORMAL ACTION BUTTONS (Match Accent Color) -------- */
div.stButton > button {{
    background-color: {ACCENT_BLUE} !important; 
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: background 0.3s ease;
}}
div.stButton > button:hover {{
    background-color: #155f8a !important; 
}}

/* FIX FOR MESSAGE ALIGNMENT IN NARROW COLUMN (History Page) */
.stAlert {{
    width: 100% !important; 
    margin-left: 0px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    border-radius: 8px !important; 
}}

/* --- NEW CSS for Blended Summary Table --- */
.formal-blended-table {{ 
    border-collapse: collapse; 
    width: 100%; 
    font-family: 'Arial', sans-serif; 
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Subtle shadow for lift */
    border-radius: 8px;
    overflow: hidden;
    margin-top: 20px; /* Add some space below the chart */
}} 
.formal-blended-table th, .formal-blended-table td {{ 
    border: 1px solid #c7d9e2; /* Light border */
    padding: 12px; 
    color: {DARK_PRIMARY} !important;
}} 
.formal-blended-table th {{ 
    background-color: {ACCENT_BLUE} !important; 
    color: white !important; 
    text-align: center; 
    font-weight: bold;
}} 
.formal-blended-table td {{ 
    /* Blend with light background by making it slightly opaque white/light-bg */
    background-color: rgba(255, 255, 255, 0.8) !important; 
    text-align: center;
}}
.formal-blended-table tr:nth-child(even) td {{ 
    /* Slightly darker stripe for readability */
    background-color: rgba(241, 247, 251, 0.8) !important;
}}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# 5. SIDEBAR LOGO AND NAVIGATION 
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Display Sidebar Logo at the top of the sidebar
if os.path.exists(SIDEBAR_LOGO_PATH):
    st.sidebar.image(SIDEBAR_LOGO_PATH) 

page = st.session_state.page

# Helper function to conditionally apply the 'active' class
def sidebar_button_with_active_state(label, target_page, icon):
    # Determine the CSS class to apply to the st.button container (div.stButton)
    class_name = "active-sidebar-button" if st.session_state.page == target_page else ""
    
    # 1. Use markdown to start a div with the desired class
    st.sidebar.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)
    
    # 2. Render the actual button inside this div
    if st.sidebar.button(label, icon=icon, key=f"nav_{target_page}"):
        st.session_state.page = target_page
        st.rerun() # Use rerun to update the page instantly
        
    # 3. Close the markdown div
    st.sidebar.markdown('</div>', unsafe_allow_html=True)


# Sidebar buttons for navigation (Using Emojis instead of icon names)
sidebar_button_with_active_state("Home", "Home", "🏠")
sidebar_button_with_active_state("Summary", "Summary", "📊")
sidebar_button_with_active_state("History", "History", "📜")


# -------------------------------
# 6. HOME PAGE
# -------------------------------
if page == "Home":
    
    # CONDITIONAL CSS INJECTION FOR HOME PAGE BACKGROUND
    if bg_base64:
        home_page_css = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{bg_base64}") !important;
            background-size: cover !important; 
            background-position: center !important;
            background-attachment: fixed !important; 
            background-repeat: no-repeat !important; 
        }}
        /* Ensure the inner block container is transparent so the fixed background is visible */
        .block-container {{
            background-image: none !important;
            background-color: transparent !important;
            overflow-y: auto !important;
        }}
        </style>
        """
        st.markdown(home_page_css, unsafe_allow_html=True)
    
    # --- Home Page Logo ---
    if os.path.exists(HOME_LOGO_PATH):
        col1, col2, col3 = st.columns([3, 1, 3]) 
        
        with col2:
            st.markdown('<div class="home-logo-container">', unsafe_allow_html=True)
            # Logo width is 100px
            st.image(HOME_LOGO_PATH, width=100) 
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("Competence Sentiment Analyzer")
    
    # Welcome message
    st.markdown(f'<p style="font-size: 16.5px; color: {DARK_PRIMARY}; margin-top: -5px; margin-bottom: 18px; text-align: center;">Welcome! The app analyzes students’ self-assessments of their Python, Java, and C programming competence using English-language sentiments.</p>', unsafe_allow_html=True)

    # BIGGER LABEL WRAP
    st.markdown("<div class='big-label'>", unsafe_allow_html=True)
    comment = st.text_area("Enter your sentiments about your programming competence:")
    st.markdown("</div>", unsafe_allow_html=True)

    # Create two columns: left for button (narrow), right for result
    col_button, col_result = st.columns([1, 2])

    with col_button:
        # The button is set to use the full width of this narrow column
        if st.button("Analyze", use_container_width=True):
            if not comment.strip():
                st.session_state.result = "Please enter some text first."
            elif model is None or vectorizer is None:
                st.session_state.result = "Model is not loaded. Cannot perform analysis."
            else:
                vectorized_comment = vectorizer.transform([comment])
                prediction = model.predict(vectorized_comment)[0]

                sentiment_labels = {
                    0: "Weak Competence",
                    1: "Normal Competence",
                    2: "Strong Competence"
                }
                st.session_state.result = sentiment_labels.get(prediction, "Unknown")

                now = datetime.now()
                pd.DataFrame({
                    "Date": [now.strftime("%Y-%m-%d")],
                    "Time": [now.strftime("%H:%M:%S")],
                    "Response": [comment],
                    "Classification": [st.session_state.result]
                }).to_csv(HISTORY_FILE, mode="a", header=False, index=False)

    with col_result:
        if "result" in st.session_state:
            if st.session_state.result == "Please enter some text first.":
                st.warning(st.session_state.result)
            elif "Model is not loaded" in st.session_state.result:
                st.error(st.session_state.result)
            else:
                st.success(f"Result: **{st.session_state.result}**")

# -------------------------------
# 7. SUMMARY PAGE (UPDATED WITH GRAPH)
# -------------------------------
elif page == "Summary":
    
    # Conditional CSS injection (ensures no background image is used)
    st.markdown("""
    <style>
    .block-container {
        background-image: none !important;
        background-color: transparent !important;
        overflow-y: auto !important; 
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Summary of Responses")
    
    # ⭐ ADDED: Insert extra vertical space after the heading
    st.markdown("<br><br>", unsafe_allow_html=True)

    # 📌 CORRECTED ALTAIR THEME CONFIGURATION
    # Fixes the jsonschema.ValidationError by defining the theme correctly
    def transparent_config_fixed():
        return {
            "config": {
                "background": "transparent",
                "view": {
                    "fill": "transparent",
                    "stroke": "transparent"
                },
                # ⭐ MODIFIED: Explicitly set axis text color to DARK_PRIMARY for contrast
                "axis": {
                    "domainColor": "#c7d9e2", # Light border (Not touched)
                    "gridColor": "#c7d9e2", # Light grid (Not touched)
                    "tickColor": "#c7d9e2", # Light tick (Not touched)
                    "labelColor": DARK_PRIMARY, # Darker label text (Numbers/Text)
                    "titleColor": DARK_PRIMARY, # Darker title text (Numbers/Text)
                },
                "header": {
                    "titleColor": DARK_PRIMARY, # Darker header title
                    "labelColor": DARK_PRIMARY, # Darker header label
                }
            }
        }
    
    alt.themes.register("transparent_bg_fixed", transparent_config_fixed)
    alt.themes.enable("transparent_bg_fixed")
    
    if os.path.exists(HISTORY_FILE):
        df_history = pd.read_csv(HISTORY_FILE)
        
        if not df_history.empty:
            
            # 1. Prepare data for charting
            sentiment_counts = df_history['Classification'].value_counts().reset_index()
            sentiment_counts.columns = ['Competence Level', 'Count']
            
            # Define the order and custom sorting (Formal order: Strong, Normal, Weak)
            order = ["Strong Competence", "Normal Competence", "Weak Competence"]
            sentiment_counts['Competence Level'] = pd.Categorical(
                sentiment_counts['Competence Level'], categories=order, ordered=True
            )
            sentiment_counts = sentiment_counts.sort_values('Competence Level')
            
            # 2. Create the Altair Bar Chart with formal styling
            chart = alt.Chart(sentiment_counts).mark_bar().encode(
                # X-axis: Competence Level, sorted by the defined order
                # title=None REMOVES the "Competence Level" text.
                x=alt.X('Competence Level', sort=order, axis=alt.Axis(title=None, labelAngle=0)), 
                # Y-axis: Count of responses
                y=alt.Y('Count', title="Number of Responses"),
                # Set a single, consistent color (ACCENT_BLUE)
                color=alt.value(ACCENT_BLUE), 
                # Tooltip ONLY shows the count of students
                tooltip=['Count'] 
            ).properties(
                # title="" REMOVES the graph title.
                title="" 
            ).interactive() # Allow zooming and panning
            
            # Display the chart
            st.altair_chart(chart, use_container_width=True)

        else:
            st.info("No sentiment data recorded yet. Submit a response on the Home page to populate this summary.")
    else:
        st.error("Error: History file not found.")


# -------------------------------
# 8. HISTORY PAGE (Re-sequenced)
# -------------------------------
elif page == "History":
    
    # CONDITIONAL CSS INJECTION FOR HISTORY PAGE (ensures no background image is used)
    st.markdown("""
    <style>
    .block-container {
        background-image: none !important;
        background-color: transparent !important;
        overflow-y: auto !important; /* Explicitly ensures scrolling works on History page */
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.subheader("History of Responses")

    if os.path.exists(HISTORY_FILE):
        df_history = pd.read_csv(HISTORY_FILE)
        
        # Display the table if it's not empty
        if not df_history.empty:
            st.markdown("""
            <style>
            .formal-table { border-collapse: collapse; width: 100%; font-family: 'Arial', sans-serif; } 
            .formal-table th, .formal-table td { border: 1px solid #c7d9e2; padding: 12px; } 
            .formal-table th { background-color: #1f7fc1; color: white; text-align: left; } 
            .formal-table td { background-color: #ffffff; }
            .formal-table tr:nth-child(even) td { background-color: #f1f7fb; }
            </style>
            """, unsafe_allow_html=True)
            st.markdown(df_history.to_html(index=False, classes="formal-table"), unsafe_allow_html=True)
        else:
            st.info("No sentiment history available.")
    else:
        st.info("History file not found.")

    # ⭐ FIX: Create two columns to align the button and the success message horizontally
    col_delete_button, col_delete_message = st.columns([1, 3]) 
    
    with col_delete_button:
        # Delete history button
        if st.button("Delete History", use_container_width=True):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
                # Success message is now shown in the second column after rerun
                st.session_state.history_deleted = True 
                st.rerun() # Use st.rerun to refresh the page content after deletion
            else:
                st.info("No history to delete.")
    
    # ⭐ FIX: Display the success message in the second column
    with col_delete_message:
        # Check if the success state is set, and display the message
        if st.session_state.get("history_deleted", False):
            # The st.success alert is placed in this column.
            # You might need to add a small vertical space (st.markdown) if the button
            # and message don't align vertically perfectly due to padding/margins.
            st.success("History successfully deleted.")
            # Important: Clear the state after showing the message so it doesn't reappear on other pages
            st.session_state.history_deleted = False 

# -------------------------------
# 9. Hide default Streamlit UI elements
# -------------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 9. Hide default Streamlit UI elements
# -------------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
