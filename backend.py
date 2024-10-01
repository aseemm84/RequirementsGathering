# backend.py
from time import sleep
import cohere
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])


def project_manager_agent(project_description, temperature):
    prompt = f"""As a project manager, provide detailed instructions for gathering initial requirements for this project:

Project Description: {project_description}

Your task:
1. Analyze the project description
2. Identify key stakeholders
3. List 5-7 specific areas to focus on for requirements gathering
4. Provide 3-5 targeted questions for each area
5. Suggest any potential challenges or considerations

Please provide a structured response with clear headings and bullet points."""
    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def stakeholder_interview_agent(instructions, temperature):
    prompt = f"""As a stakeholder interviewer, conduct simulated interviews based on these instructions and provide initial requirements:

Instructions: {instructions}

Your task:
1. Simulate interviews with key stakeholders identified
2. For each stakeholder:
    a. Introduce the stakeholder (role, perspective)
    b. List 5-7 key requirements they might have
    c. Provide any concerns or constraints they might mention
3. Summarize common themes across all interviews
4. Highlight any conflicting requirements between stakeholders

Please provide a structured response with clear headings for each stakeholder and a summary section."""
    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def requirements_analyzer_agent(initial_requirements, temperature):
    prompt = f"""As a requirements analyzer, refine and categorize these initial requirements:

Initial Requirements: {initial_requirements}

Your task:
1. Categorize requirements into:
    a. Functional Requirements
    b. Non-Functional Requirements
    c. Technical Requirements
    d. User Interface Requirements
    e. Security Requirements
2. For each category:
    a. List and number each requirement
    b. Prioritize requirements (High, Medium, Low)
    c. Identify any dependencies between requirements
3. Highlight any ambiguous or conflicting requirements
4. Suggest 3-5 additional requirements that might have been overlooked

Please provide a structured response with clear headings for each category and a summary of key findings."""
    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def documentation_agent(refined_requirements, temperature):
    prompt = f"""As a documentation specialist, compile a final requirements document based on these refined requirements:

Refined Requirements: {refined_requirements}

Your task:
1. Create an executive summary (2-3 paragraphs)
2. Provide a table of contents
3. For each category of requirements:
    a. Provide a brief introduction
    b. List all requirements in a numbered format
    c. Include priority and any dependencies for each requirement
4. Create a glossary of technical terms used
5. Add a section on assumptions and constraints
6. Include a section on future considerations or potential enhancements

Please format the document with clear headings, subheadings, and use bullet points or numbered lists where appropriate."""
    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=temperature
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def process_requirements(project_description, temperature, status_callback):
    try:
        status_callback(
            "Project Manager Agent: Generating instructions (it may take several minutes)..."
        )
        pm_instructions = project_manager_agent(project_description,
                                                temperature)

        # --- Modification starts here ---
        with st.expander("Project Manager Instructions"):
            st.write(pm_instructions)
            modify_pm = st.checkbox("Modify Project Manager Instructions?")
            if modify_pm:
                new_pm_instructions = st.text_area("Modified Instructions:",
                                                  value=pm_instructions)
                pm_instructions = new_pm_instructions
        # --- Modification ends here ---

        status_callback(
            "Stakeholder Interview Agent: Gathering initial requirements (it may take several minutes)..."
        )
        initial_requirements = stakeholder_interview_agent(pm_instructions,
                                                          temperature)

        # --- Modification starts here ---
        with st.expander("Initial Requirements"):
            st.write(initial_requirements)
            modify_initial = st.checkbox("Modify Initial Requirements?")
            if modify_initial:
                new_initial_requirements = st.text_area(
                    "Modified Initial Requirements:",
                    value=initial_requirements)
                initial_requirements = new_initial_requirements
        # --- Modification ends here ---

        status_callback(
            "Requirements Analyzer Agent: Refining and categorizing requirements (it may take several minutes)..."
        )
        refined_requirements = requirements_analyzer_agent(
            initial_requirements, temperature)

        # --- Modification starts here ---
        with st.expander("Refined Requirements"):
            st.write(refined_requirements)
            modify_refined = st.checkbox("Modify Refined Requirements?")
            if modify_refined:
                new_refined_requirements = st.text_area(
                    "Modified Refined Requirements:",
                    value=refined_requirements)
                refined_requirements = new_refined_requirements
        # --- Modification ends here ---

        status_callback(
            "Documentation Agent: Compiling final document (it may take several minutes)..."
        )
        final_document = documentation_agent(refined_requirements,
                                            temperature)

        return {
            "pm_instructions": pm_instructions,
            "initial_requirements": initial_requirements,
            "refined_requirements": refined_requirements,
            "final_document": final_document
        }
    except Exception as e:
        raise Exception(f"Error in requirements gathering process: {str(e)}")
