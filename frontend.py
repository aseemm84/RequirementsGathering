import streamlit as st
import backend
import base64
from fpdf import FPDF
import time
from datetime import datetime
import requests
from PIL import Image

# Streamlit page configuration
st.set_page_config(page_title="Vision Forge: Crafting Project Foundations", layout="wide", page_icon="📄")

# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stTextArea > div > div > textarea {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for advanced options
with st.sidebar:
    st.header("Advanced Options")
    
    # Response Style (Temperature) slider with 12 steps
    temp_options = {
        0.0: "Focused",
        0.2: "Somewhat Focused",
        0.4: "Balanced (Slightly Focused)",
        0.6: "Balanced (Slightly Creative)",
        0.8: "Creative",
        1.0: "Very Creative"
    }
    temp_value = st.select_slider(
        "Response Style",
        options=list(temp_options.keys()),
        format_func=lambda x: temp_options[x],
        value=0.4
    )
    st.caption("Adjust this to control how focused or creative the responses should be.")

    st.markdown("---")
    st.header("About Vision Forge")
    st.markdown("""
    Vision Forge is an advanced AI-powered tool designed to revolutionize the project requirements gathering process. By leveraging cutting-edge language models and a multi-agent approach, Vision Forge helps you craft robust project foundations with ease and precision.

    **Key Features:**
    - AI-driven project analysis
    - Simulated stakeholder interviews
    - Intelligent requirements categorization
    - Automated documentation generation

    Vision Forge empowers project managers, business analysts, and development teams to quickly transform vague project ideas into comprehensive, actionable requirements documents.

    Forge your project's future with clarity and insight!
    """)

    # Add version information
    st.caption("Version 1.0.0")
    
    # Add a link to more information or your website
    linkedin_url = "https://www.linkedin.com/in/aseem-mehrotra/"
    st.sidebar.markdown(f'<a href="{linkedin_url}" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png
