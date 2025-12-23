import streamlit as st 
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils import get_db_connection

st.set_page_config(page_title="E-commerce Inventory", page_icon="📦")

try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Missing config.yaml file! Please create it in the root folder.")
    st.stop()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login(location='main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    
    st.title("E-Commerce Inventory Management")
    st.write(f'# Welcome, {st.session_state["name"]}!')

    conn = get_db_connection()
    if conn and conn.is_connected():
        st.success("Connected to MySQL Database!")
        conn.close()
    else:
        st.error("Couldn't connect to MySQL. Check your secrets.toml or MySQL connection.")

    user_roles = st.session_state.get("roles", [])

    if "admin" in user_roles:
        st.success("Logged in as: ADMIN")
        st.info("Admin Tools: View logs, Edit users, Delete records.")
    else:
        st.success("Logged in as: USER")
        st.write("Standard Access: View stock and products.")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')