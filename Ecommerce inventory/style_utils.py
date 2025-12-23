import streamlit as st

def applywo_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #FFF0F5; } /* Lavender Blush */
        [data-testid="stSidebar"] { background-color: #E1F5FE !important; } /* Baby Blue */
        
        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: white;
            border-radius: 20px;
            border: 2px solid #F8BBD0;
            box-shadow: 5px 5px 15px #E3F2FD;
        }

        /* Status Tags */
        .status-fast { background-color: #BDE0FE; color: #0077B6; padding: 5px 10px; border-radius: 10px; }
        .status-slow { background-color: #FFC2D1; color: #AD1457; padding: 5px 10px; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)