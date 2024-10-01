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
logo = Image.open("logo.png")  # Replace "logo.png" with the actual path to your logo image
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
        pm_output = st.empty()  # Placeholder for the output
        pm_output.write(pm_instructions)

        # User feedback loop for Project Manager Agent
        col1, col2 = st.columns(2)  # Create columns for buttons
        pm_yes_button = col1.button("Yes", key="pm_yes")
        pm_no_button = col2.button("No", key="pm_no")
        
        while not pm_yes_button:  # Loop until "Yes" is clicked
            if pm_no_button:
                refinement_instructions = st.text_area("Please provide your concerns or any specific instructions for the Project Manager Agent:")
                pm_instructions = backend.project_manager_agent(project_description, temp_value, refinement_instructions=refinement_instructions)
                pm_output.write(pm_instructions)  # Update the output
                pm_yes_button = col1.button("Yes", key="pm_yes")  # Update button states
                pm_no_button = col2.button("No", key="pm_no")

        # --- Stakeholder Interview Agent ---
        status_placeholder = st.empty()
        status_placeholder.info("Stakeholder Interview Agent: Gathering initial requirements...")
        initial_requirements = backend.stakeholder_interview_agent(pm_instructions, temp_value)
        status_placeholder.empty()

        st.subheader("Initial Requirements:")
        si_output = st.empty()
        si_output.write(initial_requirements)

        # User feedback loop for Stakeholder Interview Agent
        col1, col2 = st.columns(2)
        si_yes_button = col1.button("Yes", key="si_yes")
        si_no_button = col2.button("No", key="si_no")

        while not si_yes_button:
            if si_no_button:
                refinement_instructions = st.text_area("Please provide your concerns or any specific instructions for the Stakeholder Interview Agent:")
                initial_requirements = backend.stakeholder_interview_agent(pm_instructions, temp_value, refinement_instructions=refinement_instructions)
                si_output.write(initial_requirements)
                si_yes_button = col1.button("Yes", key="si_yes")
                si_no_button = col2.button("No", key="si_no")

        # --- Requirements Analyzer Agent ---
        status_placeholder = st.empty()
        status_placeholder.info("Requirements Analyzer Agent: Refining and categorizing requirements...")
        refined_requirements = backend.requirements_analyzer_agent(initial_requirements, temp_value)
        status_placeholder.empty()

        st.subheader("Refined Requirements:")
        ra_output = st.empty()
        ra_output.write(refined_requirements)

        # User feedback loop for Requirements Analyzer Agent
        col1, col2 = st.columns(2)
        ra_yes_button = col1.button("Yes", key="ra_yes")
        ra_no_button = col2.button("No", key="ra_no")

        while not ra_yes_button:
            if ra_no_button:
                refinement_instructions = st.text_area("Please provide your concerns or any specific instructions for the Requirements Analyzer Agent:")
                refined_requirements = backend.requirements_analyzer_agent(initial_requirements, temp_value, refinement_instructions=refinement_instructions)
                ra_output.write(refined_requirements)
                ra_yes_button = col1.button("Yes", key="ra_yes")
                ra_no_button = col2.button("No", key="ra_no")

        # --- Documentation Agent ---
        status_placeholder = st.empty()
        status_placeholder.info("Documentation Agent: Compiling final document...")
        final_document = backend.documentation_agent(refined_requirements, temp_value)
        status_placeholder.empty()

        st.subheader("Final Requirements Document")
        doc_output = st.empty()
        doc_output.write(final_document)

        # User feedback loop for Documentation Agent
        col1, col2 = st.columns(2)
        doc_yes_button = col1.button("Yes", key="doc_yes")
        doc_no_button = col2.button("No", key="doc_no")

        while not doc_yes_button:
            if doc_no_button:
                refinement_instructions = st.text_area("Please provide your concerns or any specific instructions for the Documentation Agent:")
                final_document = backend.documentation_agent(refined_requirements, temp_value, refinement_instructions=refinement_instructions)
                doc_output.write(final_document)
                doc_yes_button = col1.button("Yes", key="doc_yes")
                doc_no_button = col2.button("No", key="doc_no")

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
