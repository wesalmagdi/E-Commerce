import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        /* Main background - Soft Blush Pink */
        .stApp {
            background-color: #FFF0F3; 
        }

        /* Sidebar - Baby Blue */
        [data-testid="stSidebar"] {
            background-color: #EBF5FF !important;
            border-right: 3px solid #D0E7FF;
        }

        /* Metric Cards - Pink with Blue Shadows */
        div[data-testid="stMetric"] {
            background-color: white;
            padding: 20px;
            border-radius: 25px;
            border: 2px solid #FFC2D1; /* Soft Pink Border */
            box-shadow: 8px 8px 0px #D0E7FF; /* Baby Blue Shadow */
        }

        /* Buttons - Deep Rose Pink */
        .stButton>button {
            background-color: #FF85A1;
            color: white;
            border-radius: 30px;
            border: none;
            font-weight: 600;
            letter-spacing: 1px;
        }
        
        .stButton>button:hover {
            background-color: #BDE0FE; /* Hover turns Baby Blue */
            color: #0077B6;
        }

        /* Re-styling Notifications: GREEN IS GONE */
        div[data-testid="stNotification"] {
            background-color: #EBF5FF !important; /* Baby Blue background */
            color: #0077B6 !important;
            border: 1px solid #BDE0FE;
            border-radius: 15px;
        }
        
        /* Table Headers - Pink */
        thead tr th {
            background-color: #FFC2D1 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)