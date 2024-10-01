import streamlit as st
import backend
import base64
from fpdf import FPDF
import time
from datetime import datetime
from PIL import Image

# Streamlit page configuration
st.set_page_config(
    page_title="Vision Forge: Crafting Project Foundations",
    layout="wide",
    page_icon="📄"
)

# Custom CSS to improve the look and feel
st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

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
    st.caption(
        "Adjust this to control how focused or creative the responses should be."
    )

    st.markdown("---")
    st.header("About Vision Forge")
    st.markdown(
        """
        Vision Forge is an advanced AI-powered tool designed to revolutionize the project requirements gathering process. By leveraging cutting-edge language models and a multi-agent approach, Vision Forge helps you craft robust project foundations with ease and precision.

        **Key Features:**
        - AI-driven project analysis
        - Simulated stakeholder interviews
        - Intelligent requirements categorization
        - Automated documentation generation

        Vision Forge empowers project managers, business analysts, and development teams to quickly transform vague project ideas into comprehensive, actionable requirements documents.

        Forge your project's future with clarity and insight!
        """
    )

    # Add version information
    st.caption("Version 1.0.0")

    # Add a link to more information or your website
    linkedin_url = "https://www.linkedin.com/in/aseem-mehrotra/"
    st.sidebar.markdown(
        f'<a href="{linkedin_url}" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="height: 30px;"></a>',
        unsafe_allow_html=True
    )

# Main content
col1, col2 = st.columns([1, 4])
# Replace "logo.png" with the actual path to your logo image
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
        start_time = time.time()
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.info(f"Process started at: {start_datetime}")

        # --- Project Manager Agent ---
        status_placeholder = st.empty()
        status_placeholder.info("Project Manager Agent: Generating instructions...")
        pm_instructions = backend.project_manager_agent(project_description, temp_value)
        status_placeholder.empty()

        st.subheader("Project Manager Instructions:")
        st.write(pm_instructions)

        # User feedback loop for Project Manager Agent
        while True:
            col1, col2 = st.columns(2)
            if col1.button("Yes", key="pm_yes"):
                break
            if col2.button("No", key="pm_no"):
                refinement_instructions = st.text_area("Please provide your concerns or any specific instructions for the Project Manager Agent:")
                pm_instructions = backend.project_manager_agent(project_description, temp_value, refinement_instructions=refinement_instructions)
                st.subheader("Updated Project Manager Instructions:")
                st.write(pm_instructions)

        # --- Stakeholder Interview Agent ---
        status_placeholder = st.empty()
        status_placeholder.info("Stakeholder Interview Agent: Gathering initial requirements...")
        initial_requirements = backend.stakeholder_interview_agent(pm_instructions, temp_value)
        status_placeholder.empty()

        st.subheader("Initial Requirements:")
        st.write(initial_requirements)

        # User feedback loop for Stakeholder Interview Agent
        while True:
            col1, col2 = st.columns(2)
            if col1.button("Yes", key="si_yes"):
                break
            if col2.button("No", key="si_no"):
                refinement_instructions = st.text_area("Please provide your concerns or any specific instructions for the Stakeholder Interview Agent:")
                initial_requirements = backend.stakeholder_interview_agent(pm_instructions, temp_value, refinement_instructions=refinement_instructions)
                st.subheader("Updated Initial Requirements:")
                st.write(initial_requirements)

        # --- Requirements Analyzer Agent ---
        status_placeholder = st.empty()
        status_placeholder.info("Requirements Analyzer Agent: Refining and categorizing requirements...")
        refined_requirements = backend.requirements_analyzer_agent(initial_requirements, temp_value)
        status_placeholder.empty()

        st.subheader("Refined Requirements:")
        st.write(refined_requirements)

        # User feedback loop for Requirements Analyzer Agent
        while True:
            col1, col2 = st.columns(2)
            if col1.button("Yes", key="ra_yes"):
                break
            if col2.button("No", key="ra_no"):
                refinement_instructions = st.text_area("Please provide your concerns or any specific instructions for the Requirements Analyzer Agent:")
                refined_requirements = backend.requirements_analyzer_agent(initial_requirements, temp_value, refinement_instructions=refinement_instructions)
                st.subheader("Updated Refined Requirements:")
                st.write(refined_requirements)

        # --- Documentation Agent ---
        status_placeholder = st.empty()
        status_placeholder.info("Documentation Agent: Compiling final document...")
        final_document = backend.documentation_agent(refined_requirements, temp_value)
        status_placeholder.empty()

        st.subheader("Final Requirements Document")
        st.write(final_document)

        # Create downloadable PDF
        pdf = create_pdf(final_document)
        st.markdown(
            get_binary_file_downloader_html(pdf, 'requirements.pdf'),
            unsafe_allow_html=True
        )

        end_time = time.time()
        end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = end_time - start_time

        st.success(f"Process completed at: {end_datetime}")
        st.info(f"Total duration: {duration:.2f} seconds")

# Footer
st.markdown("---")
st.markdown("Powered by Cohere and Streamlit")
