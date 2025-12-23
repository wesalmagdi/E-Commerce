import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        /* Main background and text */
        .stApp {
            background-color: #121212; /* Deep Charcoal */
            color: #E0E0E0;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1E1E1E;
            border-right: 1px solid #333333;
        }

        /* Metric boxes (Cards) */
        [data-testid="stMetricValue"] {
            color: #FFB6C1 !important; /* Soft Pink accents */
        }
        
        div[data-testid="metric-container"] {
            background-color: #252525;
            border: 1px solid #444;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        /* Dataframe styling */
        .stDataFrame {
            background-color: #1E1E1E;
            border-radius: 10px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #AD1457;
            color: white;
            border-radius: 20px;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #FFB6C1;
            color: #121212;
        }

        /* Titles and Headers */
        h1, h2, h3 {
            color: #FFB6C1 !important;
        }
        </style>
    """, unsafe_allow_html=True)