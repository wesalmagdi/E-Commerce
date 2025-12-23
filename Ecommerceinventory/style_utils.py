import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        /* 1. FORCE GLOBAL DARK MODE */
        .stApp, .stAppViewContainer, .stMain {
            background-color: #0E1117 !important;
            color: #FFFFFF !important;
        }

        /* 2. DARK SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #161B22 !important;
            border-right: 1px solid #30363D !important;
        }

        /* 3. WHITE TEXT FOR EVERYTHING */
        h1, h2, h3, h4, h5, h6, p, span, label, div, li, .stMarkdown {
            color: #FFFFFF !important;
        }

        /* 4. DARK TABLES & DATAFRAMES */
        .stDataFrame, .stTable, div[data-testid="stTable"] {
            background-color: #0E1117 !important;
            color: white !important;
        }
        
        /* 5. INPUT BOXES (Search bars, dropdowns) */
        .stTextInput input, .stSelectbox div {
            background-color: #21262D !important;
            color: white !important;
            border: 1px solid #30363D !important;
        }

        /* 6. BUTTONS */
        .stButton>button {
            background-color: #238636 !important;
            color: white !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)