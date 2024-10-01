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



    # # Response Length (Max Tokens) slider with 12 steps

    # token_options = {

    #     5000: "Brief",

    #     6500: "Moderate",

    #     8000: "Detailed",

    #     9500: "Extensive"

    # }

    # token_value = st.select_slider(

    #     "Response Length",

    #     options=list(token_options.keys()),

    #     format_func=lambda x: token_options[x],

    #     value=8000

    # )

    # st.caption("Adjust this to control how brief or detailed the responses should be.")

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

    st.sidebar.markdown(f'<a href="{linkedin_url}" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="height: 30px;"></a>', unsafe_allow_html=True)



# Main content

col1, col2 = st.columns([1, 4])

logo = Image.open("logo.png")

col1.image(logo, width=150)

col2.title("Vision Forge: Crafting Project Foundations")



project_description = st.text_area("Describe your project:", height=200)



def create_pdf(content):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, content)

    return pdf.output(dest="S").encode("latin-1")



def get_binary_file_downloader_html(bin_file, file_label='File'):

    bin_str = base64.b64encode(bin_file).decode()

    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}" class="download-button">Download {file_label}</a>'

    return href



if st.button("Gather Requirements"):

    if not project_description:

        st.warning("Please enter a project description.")

    else:

        try:

            start_time = time.time()

            start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.info(f"Process started at: {start_datetime}")



            # Create a placeholder for the status messages

            status_placeholder = st.empty()



            # Define a callback function to update the status

            def update_status(message):

                status_placeholder.info(message)



            # Process requirements with status updates

            results = backend.process_requirements(

                project_description,

                temp_value,

                update_status

            )

            

            # Clear the status placeholder

            status_placeholder.empty()

            

            # Display results in expandable sections

            with st.expander("Project Manager Instructions", expanded=True):

                st.write(results["pm_instructions"])

            

            with st.expander("Initial Requirements", expanded=True):

                st.write(results["initial_requirements"])

            

            with st.expander("Refined Requirements", expanded=True):

                st.write(results["refined_requirements"])

            

            st.subheader("Final Requirements Document")

            st.write(results["final_document"])

            

            # Create downloadable PDF

            pdf = create_pdf(results["final_document"])

            st.markdown(get_binary_file_downloader_html(pdf, 'requirements.pdf'), unsafe_allow_html=True)

            

            end_time = time.time()

            end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            duration = end_time - start_time



            st.success(f"Process completed at: {end_datetime}")

            st.info(f"Total duration: {duration:.2f} seconds")

            

            # Feedback mechanism

            st.write("Was this helpful?")

            col1, col2 = st.columns(2)

            with col1:

                if st.button("👍"):

                    st.success("Thanks for your feedback!")

            with col2:

                if st.button("👎"):

                    st.warning("We're sorry to hear that. Please let us know how we can improve.")

            

        except requests.exceptions.Timeout:

            st.error("The request timed out. This can happen for complex projects. Please try again with a shorter project description or adjust the Response Length to a briefer option.")

        except Exception as e:

            st.error(f"An unexpected error occurred: {str(e)}")



# Footer

st.markdown("---")

st.markdown("Powered by Cohere and Streamlit")


